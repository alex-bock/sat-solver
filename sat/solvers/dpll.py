
import copy
import time
from typing import Dict, Tuple

from ._base_solver import Solver
from ..selectors._base_selector import BaseSelector
from ._exceptions import UNSATException, TimeoutException

from ..constants import Tau, NOT
from ..formulas import CNF


class DPLL(Solver):

    def __init__(self, selector: BaseSelector, verbose: bool = False):

        super().__init__(verbose=verbose)
        self._selector = selector

        return

    def solve(self, formula: CNF, timeout: float = None) -> Tau:

        tau = {var: True for var in formula.vars}
        self._n_calls = 0
        self._timeout = timeout
        self._t_start = time.time()

        try:
            _, tau = self._solve_rec(formula, tau)
        except UNSATException:
            tau = None

        return tau

    def _solve_rec(
        self, formula: CNF, tau: Dict[str, bool], depth: int = 0
    ) -> Tuple[CNF, Tau]:

        if self._timeout is not None and (time.time() - self._t_start) > self._timeout:
            raise TimeoutException

        if len(formula) == 0:
            return formula, tau
        elif formula.has_empty_clauses():
            if self._verbose:
                print(" " * depth, "empty clauses found!")
            raise UNSATException

        if formula.has_unit_clauses():
            reduced_formula, updated_tau = self._unit_propagate(
                formula, tau, depth=depth
            )
            return self._solve_rec(
                reduced_formula, updated_tau, depth=depth + 1
            )
        else:
            try:
                var, val = self._selector.select(formula)
                reduced_formula, updated_tau = self._split(
                    formula, var, val, tau, depth=depth
                )
                return self._solve_rec(
                    reduced_formula, updated_tau, depth=depth + 1
                )
            except UNSATException:
                if self._verbose:
                    print(" " * depth, "backtracking...")
                reduced_formula, updated_tau = self._split(
                    formula, var, not val, tau, depth=depth
                )
                return self._solve_rec(
                    reduced_formula, updated_tau, depth=depth + 1
                )

    def _unit_propagate(
        self, formula: CNF, tau: Tau, depth: int = 0
    ) -> Tuple[CNF, Tau]:

        unit_clauses = formula.get_unit_clauses()

        literal = unit_clauses[0][0]
        if literal.startswith(NOT):
            var = literal[1:]
            val = False
        else:
            var = literal
            val = True

        if self._verbose:
            print(" " * depth, "propagating...", len(formula), var, val)

        assignment = {var: val}
        reduced_formula = copy.deepcopy(formula)
        reduced_formula.reduce(assignment)

        updated_tau = copy.deepcopy(tau)
        updated_tau.update(assignment)

        return reduced_formula, updated_tau

    def _split(
        self, formula: CNF, var: str, val: bool, tau: Tau, depth: int = 0
    ) -> Tuple[CNF, Tau]:

        if self._verbose:
            print(" " * depth, "splitting...", len(formula), var, val)
        self._n_calls += 1

        assignment = {var: val}
        reduced_formula = copy.deepcopy(formula)
        reduced_formula.reduce(assignment)

        updated_tau = copy.deepcopy(tau)
        updated_tau.update(assignment)

        return reduced_formula, updated_tau
