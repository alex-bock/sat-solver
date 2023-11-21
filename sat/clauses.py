
from typing import Self

from .constants import LP, RP, OR, AND


class Clause:

    sym = None

    def __init__(self, *literals):

        self.literals = list(literals)

        return
    
    def __getitem__(self, idx: int) -> str:

        return self.literals[idx]
    
    def __iter__(self):

        return iter(self.literals)
    
    def __len__(self) -> int:

        return len(self.literals)
    
    def __repr__(self) -> str:

        s = LP + self.sym.join(self.literals) + RP

        if self.is_unit():
            return s[1:-1]
        else:
            return s
        
    def is_empty(self) -> bool:

        return len(self) == 0
    
    def is_unit(self) -> bool:

        return len(self) == 1
    
    def is_equivalent(self, clause: Self) -> bool:

        return set(self.literals) == set(clause.literals)


class Disjunction(Clause):

    sym = OR
    

class Conjunction(Clause):

    sym = AND