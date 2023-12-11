
from ._base_selector import BaseSelector
from .random_choice import RandomChoiceSelector
from ..formulas import CNF
from ..constants import NOT


class TwoClauseSelector(BaseSelector):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fallback_selector = RandomChoiceSelector()

        return

    def select(self, formula: CNF) -> (str, bool):

        # print(len([clause for clause in formula if len(clause) == 2]))

        selection = None
        for var in formula.vars:
            clauses = [
                clause for clause in formula
                if (
                    var in clause.literals or f"{NOT}{var}" in clause.literals
                )
            ]
            # print(var, clauses)
            if len(clauses) > 0 and \
               max([len(clause) for clause in clauses]) == 2:
                selection = (var, True)
                break

        if selection is None:
            # print("falling back")
            selection = self.fallback_selector.select(formula)
        # print(selection)

        return selection
