
import abc

from ..formulas import ClausalFormula


class Solver:

    def __init__(self, verbose: bool = False):

        self._verbose = verbose
        self._n_calls = 0

        return

    @abc.abstractmethod
    def solve(self, formula: ClausalFormula):

        raise NotImplementedError
