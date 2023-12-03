
from ._base_selector import BaseSelector
from ..formulas import CNF


class NaiveSelector(BaseSelector):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        return

    def select(self, formula: CNF) -> (str, bool):

        lit = formula[0][0]
        val = self.assign(lit)
        var = self._lit_to_var(lit)

        return (var, val)
