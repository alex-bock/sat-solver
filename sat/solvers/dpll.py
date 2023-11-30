
import copy
from typing import Dict, Tuple

from ._base_solver import Solver
from ._exceptions import UNSATExcpetion

from ..constants import Tau, NOT
from ..formulas import CNF


class DPLL(Solver):

    def __init__(self):

        super().__init__()

        return

    def solve(self, formula: CNF) -> Tau:

        tau = dict()
        _, tau = self._solve_rec(formula, tau)

        return tau

    def _solve_rec(
        self, formula: CNF, tau: Dict[str, bool], depth: int = 0
    ) -> Tuple[CNF, Tau]:

        if len(formula) == 0:
            return formula, tau
        elif formula.has_empty_clauses():
            print(" " * depth, "empty clauses found!")
            raise UNSATExcpetion

        if formula.has_unit_clauses():
            reduced_formula, updated_tau = self._unit_propagate(
                formula, tau, depth=depth
            )
            return self._solve_rec(
                reduced_formula, updated_tau, depth=depth + 1
            )
        else:
            try:
                reduced_formula, updated_tau = self._split(
                    formula, tau, True, depth=depth
                )
                return self._solve_rec(
                    reduced_formula, updated_tau, depth=depth + 1
                )
            except UNSATExcpetion:
                print(" " * depth, "backtracking...")
                reduced_formula, updated_tau = self._split(
                    formula, tau, False, depth=depth
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

        print(" " * depth, "propagating...", len(formula), var, val)

        assignment = {var: val}
        reduced_formula = copy.deepcopy(formula)
        reduced_formula.reduce(assignment)

        updated_tau = copy.deepcopy(tau)
        updated_tau.update(assignment)

        return reduced_formula, updated_tau

    def _split(
        self, formula: CNF, tau: Tau, val: bool, depth: int = 0
    ) -> Tuple[CNF, Tau]:

        literal = formula[0][0]
        if literal.startswith(NOT):
            var = literal[1:]
        else:
            var = literal

        print(" " * depth, "splitting...", len(formula), var, val)

        assignment = {var: val}
        reduced_formula = copy.deepcopy(formula)
        reduced_formula.reduce(assignment)

        updated_tau = copy.deepcopy(tau)
        updated_tau.update(assignment)

        return reduced_formula, updated_tau


if __name__ == "__main__":

    cnf = CNF.from_dimacs("./input/UUF50.218.1000/uuf50-05.cnf")

    solver = DPLL()
    tau = solver.solve(cnf)
