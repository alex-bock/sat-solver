
from unittest import TestCase

from sat.solvers import DPLL
from sat.selectors import NaiveSelector
from sat.formulas import CNF
from sat.solvers._exceptions import UNSATException


SIMPLE_SAT = "p0 ∧ ¬p1"
SIMPLE_UNSAT = "p0 ∧ ¬p0"
COMPLEX_SAT = "(p0 v ¬p1) ∧ (¬p2 v ¬p3)"
COMPLEX_SAT_MULT_OCCUR = "(p0 v ¬p1) ∧ (p2 v ¬p3) ∧ (p1 v ¬p2)"
COMPLEX_SAT_BACKTRACK = "(p2 v ¬p1 v p0) ∧ (¬p2 v p3) ∧ (¬p2 v ¬p3)"


class TestDPLL(TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.solver = DPLL(selector=NaiveSelector())

        return

    def test_solve_simple_sat(self):

        cnf = CNF.from_str(SIMPLE_SAT)
        tau = self.solver.solve(cnf)

        self.assertDictEqual(tau, {"p0": True, "p1": False})
        self.assertTrue(cnf.evaluate(tau))

        return

    def test_solve_simple_unsat(self):

        cnf = CNF.from_str(SIMPLE_UNSAT)

        with self.assertRaises(UNSATException):
            self.solver.solve(cnf)

        return

    def test_solve_complex_sat(self):

        cnf = CNF.from_str(COMPLEX_SAT)
        tau = self.solver.solve(cnf)

        self.assertDictEqual(
            tau, {"p0": True, "p1": True, "p2": False, "p3": True}
        )
        self.assertTrue(cnf.evaluate(tau))

        return

    def test_solve_complex_sat_multiple_occurrences(self):

        cnf = CNF.from_str(COMPLEX_SAT_MULT_OCCUR)
        tau = self.solver.solve(cnf)

        self.assertDictEqual(
            tau, {"p0": True, "p1": True, "p2": True, "p3": True}
        )
        self.assertTrue(cnf.evaluate(tau))

        return

    def test_solve_complex_sat_backtrack(self):

        cnf = CNF.from_str(COMPLEX_SAT_BACKTRACK)
        tau = self.solver.solve(cnf)

        self.assertDictEqual(
            tau, {"p0": True, "p1": False, "p2": False, "p3": True}
        )
        self.assertTrue(cnf.evaluate(tau))

        return
