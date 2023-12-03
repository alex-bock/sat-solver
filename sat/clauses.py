
import abc
from typing import List, Self

from .constants import LP, RP, OR, AND, NOT


class Clause(abc.ABC):

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

    @property
    @abc.abstractmethod
    def sym(self) -> str:

        raise NotImplementedError

    def is_empty(self) -> bool:

        return len(self) == 0

    def is_unit(self) -> bool:

        return len(self) == 1

    def is_equivalent(self, clause: Self) -> bool:

        return set(self.literals) == set(clause.literals)


class Conjunction(Clause):

    sym = AND


class Disjunction(Clause):

    sym = OR

    def to_dimacs(self, var_map: dict) -> List[int]:

        dimacs = list()

        for lit in self.literals:
            if lit.startswith(NOT):
                dimacs.append(-1 * var_map[lit[1:]])
            else:
                dimacs.append(var_map[lit])

        return dimacs
