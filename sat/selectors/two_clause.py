
from ._base_selector import BaseSelector
from ..formulas import CNF


class TwoClauseSelector(BaseSelector):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        return

    def select(self, formula: CNF) -> str:

        raise NotImplementedError
