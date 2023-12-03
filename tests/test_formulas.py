
from unittest import TestCase

from sat.formulas import CNF, DNF
from sat.clauses import Disjunction
from sat.constants import NOT


TEST_CNF_CLAUSES = [
    ["¬p0", "p1", "¬p2"],
    ["¬p3", "¬p4", "p5"],
    ["p6", "¬p7", "¬p8"],
    ["p9", "p10", "¬p11"],
    ["p12", "¬p13", "p14"]
]
TEST_CNF_N_VARS = 15
TEST_ADD_CLAUSE = ["p14", "p15", "p16"]
TEST_APPEND_CNF_CLAUSES = [
    ["p15", "p16", "p17"],
    ["p18", "p19", "p20"]
]

TEST_DNF_STR = "(p0 ∧ p1 ∧ p2) v (p3 ∧ p4 ∧ p5)"
TEST_DNF_CLAUSE_LEN = 3
TEST_DNF_LEN = 2

TEST_DIMACS_FP = "./tests/artifacts/test_dimacs.txt"
TEST_DIMACS_LITERALS = ["p1", "p2", "p3", "p4", "p5", "p6"]


class TestCNF(TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )

        return
    
    def test_properties(self):

        self.assertEqual(len(self.cnf), len(TEST_CNF_CLAUSES))
        self.assertEqual(len(self.cnf.vars), TEST_CNF_N_VARS)

        return
    
    def test_from_dimacs(self):

        cnf = CNF.from_dimacs(TEST_DIMACS_FP)

        self.assertSetEqual(cnf.vars, set(TEST_DIMACS_LITERALS))

        return
    
    def test_from_dnf(self):

        dnf = DNF.from_str(TEST_DNF_STR)
        cnf = CNF.from_dnf(dnf)

        self.assertEqual(len(cnf), TEST_DNF_CLAUSE_LEN ** TEST_DNF_LEN)
        self.assertSetEqual(dnf.vars, cnf.vars)

        return

    def test_generate(self):

        n_vars = 20
        n_clauses = 5
        cnf = CNF.generate(n=n_vars, l=n_clauses)

        self.assertEqual(len(cnf), n_clauses)
        for clause in cnf:
            self.assertEqual(len(clause), 3)

        return
    
    def test_add_clause(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.add_clause(*TEST_ADD_CLAUSE)

        self.assertEqual(len(cnf), len(TEST_CNF_CLAUSES) + 1)
        self.assertEqual(len(cnf.vars), TEST_CNF_N_VARS + 2)

        return
    
    def test_append_cnf(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.append_cnf(
            CNF([Disjunction(*literals) for literals in TEST_APPEND_CNF_CLAUSES])
        )

        self.assertEqual(len(cnf), len(TEST_CNF_CLAUSES) + 2)
        self.assertEqual(len(cnf.vars), TEST_CNF_N_VARS + 6)

        return
    
    def test_has_empty_clauses(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.add_clause()

        self.assertTrue(cnf.has_empty_clauses())

        return

    def test_unit_clauses(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.add_clause("p15")

        self.assertTrue(cnf.has_unit_clauses())
        self.assertEqual(len(cnf.get_unit_clauses()), 1)

        return
    
    def test_simplify(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.add_clause(*TEST_CNF_CLAUSES[0])
        cnf.simplify()

        self.assertEqual(len(cnf), len(TEST_CNF_CLAUSES))

        return
    
    def test_reduce(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.reduce({"p0": True})

        self.assertEqual(len(cnf), len(TEST_CNF_CLAUSES))
        self.assertEqual(len(cnf[0]), len(TEST_CNF_CLAUSES[0]) - 1)

        return
    
    def test_reduce_drop_clause(self):

        cnf = CNF(
            [Disjunction(*literals) for literals in TEST_CNF_CLAUSES]
        )
        cnf.reduce({"p0": False})

        self.assertEqual(len(cnf), len(TEST_CNF_CLAUSES) - 1)

        return
    
    def test_evaluate_partial(self):

        tau = {}
        for clause in self.cnf:
            for lit in clause:
                if lit.startswith(NOT):
                    tau[lit[1:]] = True
                else:
                    tau[lit] = True
        
        self.assertTrue(self.cnf.evaluate(tau))

        return
    
    def test_evaluate_complete(self):

        tau = {}
        for clause in self.cnf:
            for lit in clause:
                if lit.startswith(NOT):
                    tau[lit[1:]] = False
                else:
                    tau[lit] = True
        
        self.assertTrue(self.cnf.evaluate(tau))

        return
    
    def test_unsatisfied(self):

        tau = {}
        for clause in self.cnf:
            for lit in clause:
                if lit.startswith(NOT):
                    tau[lit[1:]] = True
                else:
                    tau[lit] = False
        
        self.assertFalse(self.cnf.evaluate(tau))

        return
