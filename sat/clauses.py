
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

    def __str__(self) -> int:

        s = LP + self.sym.join(self.literals) + RP

        if self.is_unit():
            return s[1:-1]
        else:
            return s

    def __repr__(self) -> str:

        return str(self)

    @abc.abstractproperty
    def sym(self) -> str:

        raise NotImplementedError

    def is_empty(self) -> bool:

        return len(self) == 0

    def is_unit(self) -> bool:

        return len(self) == 1

    def is_equivalent(self, clause: Self) -> bool:

        return set(self.literals) == set(clause.literals)

    def remove(self, *literals):

        for lit in literals:
            while lit in self:
                self.literals.remove(lit)

        return


class Conjunction(Clause):

    @classmethod
    @property
    def sym(self) -> str:

        return AND


class Disjunction(Clause):

    @classmethod
    @property
    def sym(self) -> str:

        return OR

    def to_dimacs(self, var_map: dict = None) -> List[int]:

        if var_map is None:
            var_map = {}
            for i in range(len(self)):
                if self[i].startswith(NOT):
                    var_map[self[i][1:]] = i
                else:
                    var_map[self[i]] = i

        dimacs = list()

        for lit in self.literals:
            if lit.startswith(NOT):
                dimacs.append("-" + str(var_map[lit[1:]]))
            else:
                dimacs.append(var_map[lit])

        return " ".join([str(x) for x in dimacs])
