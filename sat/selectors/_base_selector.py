
import abc

from ..formulas import CNF


class BaseSelector(abc.ABC):

    def __init__(self):

        return

    @abc.abstractclassmethod
    def select(self, formula: CNF) -> str:

        raise NotImplementedError
