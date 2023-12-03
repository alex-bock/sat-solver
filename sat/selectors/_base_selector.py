
import abc

from ..formulas import CNF
from ..constants import NOT


class BaseSelector(abc.ABC):

    def __init__(self):

        return

    @abc.abstractclassmethod
    def select(self, formula: CNF) -> (str, bool):

        raise NotImplementedError
    
    def _lit_to_var(self, lit: str) -> str:

        if lit.startswith(NOT):
            var = lit[1:]
        else:
            var = lit

        return var

    def assign(self, lit: str) -> bool:

        return not lit.startswith(NOT)
