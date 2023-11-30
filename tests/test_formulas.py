
from unittest import TestCase

from sat.formulas import CNF


CNF_STR = "(¬p11 v p4 v ¬p0) ∧ (¬p5 v ¬p5 v p17) ∧ (p6 v ¬p1 v ¬p12) ∧ (p8 v p0 v ¬p17) ∧ (p12 v ¬p8 v p16)"
CNF_LEN = 5


class TestCNF(TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        return
    
    def test_from_str(self):

        cnf = CNF.from_str(CNF_STR)

        self.assertEqual(cnf.as_str(), CNF_STR)
        self.assertEqual(len(cnf), CNF_LEN)

        return
    
    def test_generate(self):

        cnf = CNF.generate(n=20, l=5)

        self.assertEqual(len(cnf), 5)
        for clause in cnf:
            self.assertEqual(len(clause), 3)
