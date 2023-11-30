
from ._base_selector import BaseSelector
from ..formulas import CNF


class NaiveSelector(BaseSelector):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        return

    def select(self, formula: CNF) -> str:

        return formula[0][0]
