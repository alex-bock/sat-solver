
import abc
from typing import List, Self, Set

import numpy as np

from .clauses import Conjunction, Disjunction
from .constants import NOT, Tau


class ClausalFormula(abc.ABC):

    def __init__(self, clauses: List = None):

        if clauses is None:
            clauses = list()

        self.clauses = clauses
        self._var_map = dict()
        self._n_vars = 0

        for clause in self.clauses:
            self._update_var_map(clause.literals)

        return

    @classmethod
    def from_str(cls, s: str) -> Self:

        phi = cls()
        for clause_str in s.split(phi._clause_connective.sym):
            if phi._literal_connective.sym in clause_str:
                phi.add_clause(
                    *clause_str[1:-1].split(phi._literal_connective.sym)
                )
            else:
                phi.add_clause(clause_str)

        return phi

    def __getitem__(self, idx: int) -> Disjunction:

        return self.clauses[idx]

    def __iter__(self):

        return iter(self.clauses)

    def __len__(self) -> int:

        return len(self.clauses)

    def __str__(self) -> str:

        return self._clause_connective.sym.join(
            [str(c) for c in self.clauses]
        )

    def __repr__(self) -> str:

        return str(self)

    @property
    @abc.abstractproperty
    def _clause_connective(self):

        raise NotImplementedError

    @property
    @abc.abstractproperty
    def _literal_connective(self):

        raise NotImplementedError

    @property
    def vars(self) -> Set[str]:

        return set(self._var_map.keys())

    def add_clause(self, *literals):

        self.clauses.append(self._literal_connective(*literals))
        self._update_var_map(literals)

        return

    def _update_var_map(self, literals: List[str]):

        for literal in literals:
            if literal.startswith(NOT):
                literal = literal[1:]
            if literal not in self._var_map.keys():
                self._n_vars += 1
                self._var_map[literal] = self._n_vars

        return

    def has_empty_clauses(self) -> bool:

        return any([clause.is_empty() for clause in self])

    def has_unit_clauses(self) -> bool:

        return any([clause.is_unit() for clause in self])

    def get_unit_clauses(self) -> Set[str]:

        return [clause for clause in self if clause.is_unit()]


class DNF(ClausalFormula):

    @property
    def _clause_connective(self):

        return Disjunction

    @property
    def _literal_connective(self):

        return Conjunction


class CNF(ClausalFormula):

    @classmethod
    def from_dimacs(cls, fp: str) -> Self:

        cnf = cls()

        with open(fp, "r") as f:
            dimacs_clauses = [line.strip() for line in f.readlines()]

        for dimacs_clause in dimacs_clauses:
            if dimacs_clause[0] in ("c", "p"):
                continue
            elif dimacs_clause[0] == "%":
                break
            literals = []
            for i_str in dimacs_clause.split():
                i = int(i_str)
                if i > 0:
                    literals.append(f"p{i}")
                elif i < 0:
                    literals.append(f"{NOT}p{abs(i)}")
            cnf.add_clause(*literals)

        return cnf

    @classmethod
    def from_dnf(cls, dnf: DNF) -> Self:

        cnf = cls()
        dnf_clauses = [clause.literals for clause in dnf]
        for cnf_clause in CNF._build_clause_from_dnf(dnf_clauses):
            cnf.add_clause(*cnf_clause)

        return cnf

    @staticmethod
    def _build_clause_from_dnf(dnf_clauses):

        if len(dnf_clauses) == 1:
            for literal in dnf_clauses[0]:
                yield [literal]
        else:
            for literal in dnf_clauses[0]:
                for x in CNF._build_clause_from_dnf(dnf_clauses[1:]):
                    yield [literal] + x

    @classmethod
    def generate(cls, n: int, l: int, k: int = 3) -> Self:

        domain = [f"p{i}" for i in range(n)]
        cnf = cls()

        for _ in range(l):
            vars = np.random.choice(domain, size=k, replace=False)
            lits = [
                f"{NOT}{var}"
                if np.random.uniform() > 0.5 else var
                for var in vars
            ]
            cnf.add_clause(*lits)

        return cnf

    @property
    def _clause_connective(self):

        return Conjunction

    @property
    def _literal_connective(self):

        return Disjunction

    def append_cnf(self, cnf: Self):

        for clause in cnf:
            self.add_clause(*clause.literals)

        return

    def simplify(self):

        i = 0
        n = 0
        while i < len(self):
            clause_i = self[i]
            j = i + 1
            while j < len(self):
                clause_j = self[j]
                if clause_i.is_equivalent(clause_j):
                    self.clauses.remove(clause_j)
                    n += 1
                else:
                    j += 1
            i += 1

        print(f"Removed {n} clauses")

        return

    def reduce(self, tau: Tau):

        i = 0
        # n = 0
        while i < len(self):
            clause = self[i]
            # print(i)
            remove = False
            # print(clause)
            for var, val in tau.items():
                # import pdb; pdb.set_trace()
                # if n == 2 and var == "p2":
                #     import pdb; pdb.set_trace()
                if val:
                    if var in clause.literals:
                        remove = True
                    else:
                        clause.remove(f"{NOT}{var}")
                        # print(f"- Changed: {clause}")
                else:
                    if f"{NOT}{var}" in clause.literals:
                        remove = True
                    else:
                        clause.remove(var)
                        # print(f"- Changed: {clause}")
            if remove:
                self.clauses.remove(clause)
                # print("- Removed")
            else:
                i += 1
            # n += 1

        return

    def evaluate(self, tau: Tau):

        result = True
        for clause in self:
            clause_result = False
            for literal in clause:
                if literal.startswith(NOT):
                    var = literal[1:]
                    if var not in tau:
                        continue
                    clause_result |= not tau[var]
                else:
                    var = literal
                    if var not in tau:
                        continue
                    clause_result |= tau[var]
            result &= clause_result

        return result

    def to_dimacs(self, fp: str):

        with open(fp, "w") as f:
            f.write(f"p cnf {self._n_vars} {len(self)}\n")
            for clause in self:
                f.write(clause.to_dimacs(var_map=self._var_map) + "\n")

        return
