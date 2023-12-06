
from collections import defaultdict

from ._base_selector import BaseSelector
from ..formulas import CNF
from ..constants import NOT


class ModalVariableSelector(BaseSelector):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        return
    
    def select(self, formula: CNF) -> (str, bool):

        pos_occ = defaultdict(int)
        neg_occ = defaultdict(int)
        max_occ = 0
        modal_var = None

        for clause in formula:
            for lit in clause:
                if lit.startswith(NOT):
                    var = lit[1:]
                    neg_occ[var] += 1
                else:
                    var = lit
                    pos_occ[var] += 1
                if pos_occ[var] + neg_occ[var] > max_occ:
                    max_occ = pos_occ[var] + neg_occ[var]
                    modal_var = var

        return (modal_var, pos_occ[modal_var] > neg_occ[modal_var])