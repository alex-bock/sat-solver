
import numpy as np

from ._base_selector import BaseSelector
from ..formulas import CNF


class RandomChoiceSelector(BaseSelector):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        return

    def select(self, formula: CNF) -> (str, bool):

        clause_i = np.random.randint(0, high=len(formula))
        lit_i = np.random.randint(0, high=len(formula[clause_i]))
        lit = formula[clause_i][lit_i]

        val = self.assign(lit)
        var = self._lit_to_var(lit)

        return (var, val)
