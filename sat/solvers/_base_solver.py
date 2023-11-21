
import abc

from ..formulas import ClausalFormula


class Solver:

    def __init__(self):

        return
    
    @abc.abstractmethod
    def solve(self, formula: ClausalFormula):

        raise NotImplementedError
