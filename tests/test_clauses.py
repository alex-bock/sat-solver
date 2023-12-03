
from unittest import TestCase

from sat.clauses import Conjunction, Disjunction
from sat.constants import NOT


TEST_LITERALS = [f"{NOT}x", "y", "z"]
EXP_DIMACS = "-0 1 2"


class TestConjunction(TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.conjunction = Conjunction(*TEST_LITERALS)

        return

    def test_properties(self):

        self.assertEqual(self.conjunction[0], TEST_LITERALS[0])
        self.assertEqual(len(self.conjunction), len(TEST_LITERALS))

        return
    
    def test_is_empty(self):

        conjunction = Conjunction(*TEST_LITERALS)
        conjunction.remove(*TEST_LITERALS)
        self.assertTrue(conjunction.is_empty())

        return
    
    def test_is_unit(self):

        conjunction = Conjunction(TEST_LITERALS[0])
        self.assertTrue(conjunction.is_unit())

        return
    
    def test_is_equivalent(self):

        conjunction = Conjunction(*TEST_LITERALS)
        self.assertTrue(self.conjunction, conjunction)

        return


class TestDisjunction(TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.disjunction = Disjunction(*TEST_LITERALS)

        return
    
    def test_to_dimacs(self):

        self.assertEqual(self.disjunction.to_dimacs(), EXP_DIMACS)

        return
