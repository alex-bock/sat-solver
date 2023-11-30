
from typing import Dict

from .constants import NOT
from .formulas import CNF, DNF


class Puzzle(object):

    def __init__(self, n: int, vals: Dict[str, str]):

        self._n = n

        if any([len(vals[cat]) != self._n for cat in vals.keys()]):
            raise Exception
        self._vals = vals

        self.rules = list()
        self._exclude_duplicates()

        return

    def _prop(self, cat: str, val: str, pos: int, neg: bool = False) -> str:

        if cat not in self._vals.keys() or val not in self._vals[cat]:
            raise Exception

        prop = f"p{cat}{val}{pos}"
        if neg:
            prop = NOT + prop

        return prop

    def _exclude_duplicates(self):

        self._baseline_rules = CNF()

        # ensure no value can occur at two houses simultaneously
        for cat in self._vals.keys():
            cat_rule = CNF()
            for val in self._vals[cat]:
                val_rule = CNF()
                val_rule.add_clause(
                    *[self._prop(cat, val, i) for i in range(self._n)]
                )
                for i in range(0, self._n):
                    for j in range(i + 1, self._n):
                        val_rule.add_clause(
                            self._prop(cat, val, i, neg=True),
                            self._prop(cat, val, j, neg=True)
                        )
                cat_rule.append_cnf(val_rule)
            self._baseline_rules.append_cnf(cat_rule)

        # ensure two values can occur at no house simultaneously
        for cat in self._vals.keys():
            cat_rule = CNF()
            for pos in range(self._n):
                pos_rule = CNF()
                pos_rule.add_clause(
                    *[self._prop(cat, val, pos) for val in self._vals[cat]]
                )
                for i_1 in range(0, len(self._vals[cat])):
                    val_1 = self._vals[cat][i_1]
                    for i_2 in range(i_1 + 1, len(self._vals[cat])):
                        val_2 = self._vals[cat][i_2]
                        pos_rule.add_clause(
                            self._prop(cat, val_1, pos, neg=True),
                            self._prop(cat, val_2, pos, neg=True)
                        )
                # import pdb; pdb.set_trace()
                cat_rule.append_cnf(pos_rule)
            # import pdb; pdb.set_trace()
            self._baseline_rules.append_cnf(cat_rule)

        # import pdb; pdb.set_trace()

        return

    def location(self, cat: str, val: str, pos: int):

        rule = DNF()
        rule.add_clause(self._prop(cat, val, pos))
        self.rules.append(rule)

        return

    def coincidence(self, cat_a: str, val_a: str, cat_b: str, val_b: str):

        rule = DNF()

        for i in range(self._n):
            rule.add_clause(
                self._prop(cat_a, val_a, i), self._prop(cat_b, val_b, i)
            )

        self.rules.append(rule)

        return

    def adjacent(self, cat_a: str, val_a: str, cat_b: str, val_b: str):

        rule = DNF()

        for i in range(self._n - 1):
            rule.add_clause(
                self._prop(cat_a, val_a, i), self._prop(cat_b, val_b, i + 1)
            )
            rule.add_clause(
                self._prop(cat_a, val_a, i + 1), self._prop(cat_b, val_b, i)
            )

        self.rules.append(rule)

        return

    def consecutive(self, cat_1: str, val_1: str, cat_2: str, val_2: str):

        rule = DNF()

        for i in range(self._n - 1):
            rule.add_clause(
                self._prop(cat_1, val_1, i), self._prop(cat_2, val_2, i + 1)
            )

        self.rules.append(rule)

        return

    @property
    def cnf(self) -> CNF:

        cnf = CNF()

        for rule in self.rules:
            cnf.append_cnf(CNF.from_dnf(rule))

        cnf.append_cnf(self._baseline_rules)
        cnf.simplify()

        return cnf
