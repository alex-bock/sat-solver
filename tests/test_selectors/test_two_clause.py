
import glob
import json
import os
from unittest import TestCase

from sat.solvers import DPLL
from sat.selectors import TwoClauseSelector
from sat.formulas import CNF


TEST_DATASET_PATH = "./tests/artifacts/test_cnfs/"
RANDOM_RESULT_PATH = "./tests/artifacts/random_result.json"


class TestTwoClauseSelector(TestCase):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.solver = DPLL(selector=TwoClauseSelector())

        self.cnfs = []
        for cnf_fp in glob.glob(os.path.join(TEST_DATASET_PATH, "*.cnf")):
            self.cnfs.append((CNF.from_dimacs(cnf_fp)))

        with open(RANDOM_RESULT_PATH, "r") as f:
            self.exp_results = json.load(f)["results"]

        return

    def test_modal_variable_selector(self):

        results = [self.solver.solve(cnf) is not None for cnf in self.cnfs]
        self.assertListEqual(
            results, [exp_result["result"] for exp_result in self.exp_results]
        )

        return
