
from dataclasses import dataclass, asdict
import glob
import json
from multiprocessing import Pool
import os
import time
from typing import Dict, List, Self

import numpy as np

from .formulas import CNF
from .solvers import DPLL
from .solvers._exceptions import TimeoutException
from .selectors import BaseSelector


@dataclass
class Result:

    result: bool
    runtime: float
    n_calls: int


DATASET_SIZE = 100


class Dataset:

    def __init__(self):

        self.formulas = list()
        self.config = dict()
        self.path = None

        return

    @classmethod
    def from_cache(cls, dir_path: str) -> Self:

        dataset = cls()

        if not os.path.exists(dir_path):
            raise ValueError

        dataset.path = dir_path

        for cnf_fp in glob.glob(os.path.join(dir_path, "*.cnf")):
            dataset.formulas.append(CNF.from_dimacs(cnf_fp))

        with open(os.path.join(dir_path, "config.json"), "r") as f:
            dataset.config = json.load(f)

        return dataset

    @classmethod
    def generate(cls, n_vars: int, n_clauses: int) -> Self:

        dataset = cls()
        dataset.config["n"] = n_vars
        dataset.config["l"] = n_clauses

        dataset._generate_formulas(DATASET_SIZE)

        return dataset

    def _generate_formulas(self, n: int):

        for _ in range(n):
            cnf = CNF.generate(n=self.config["n"], l=self.config["l"])
            self.formulas.append(cnf)

        return

    def write(self, path: str, overwrite: bool = False):

        if os.path.exists(path) and not overwrite:
            raise ValueError
        elif not os.path.exists(path):
            os.makedirs(path)

        self.path = path

        for i in range(len(self)):
            self[i].to_dimacs(os.path.join(self.path, f"f{i}.cnf"))

        with open(os.path.join(self.path, "config.json"), "w") as f:
            json.dump(self.config, f)

        return

    def __len__(self) -> int:

        return len(self.formulas)

    def __getitem__(self, idx: int) -> CNF:

        return self.formulas[idx]


class Experiment:

    def __init__(
        self,
        selector: BaseSelector,
        n_vars: int,
        min_ratio: float,
        max_ratio: float,
        ratio_step: float
    ):

        self.selector = selector

        self.n_vars = n_vars
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.ratio_step = ratio_step

        return

    def run(self, outpath: str, data_path: str = "./datasets/", n_iter: int = 100):

        dataset_path = os.path.join(data_path, f"n={self.n_vars}")
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
        ratios = np.arange(
            start=self.min_ratio, stop=self.max_ratio, step=self.ratio_step
        )

        for ratio in ratios:
            l = int(ratio * self.n_vars)
            self._run_experiment(
                dataset_path,
                l,
                n_iter,
                os.path.join(outpath, f"n={self.n_vars}")
            )

        return

    def _run_experiment(
        self, dataset_path: str, l: int, n_iter: int, outpath: str
    ):

        print("Loading dataset...")
        dataset = self._get_dataset(os.path.join(dataset_path, f"l={l}"), l)

        assert len(dataset) >= n_iter

        print("Starting...")
        results = Pool(processes=4).starmap(
            self._solve_formula,
            [[formula] for formula in dataset.formulas[:n_iter]]
        )
        self._write_results(results, l, dataset.config, outpath)

        return

    def _get_dataset(self, dataset_path: str, l: int) -> Dataset:

        if not os.path.exists(dataset_path):
            print(f"Generating dataset for n={self.n_vars}, l={l}")
            dataset = Dataset.generate(n_vars=self.n_vars, n_clauses=l)
            print(f"- {dataset_path}")
            dataset.write(dataset_path)

        dataset = Dataset.from_cache(dataset_path)

        return dataset

    def _solve_formula(self, formula: CNF):

        solver = DPLL(selector=self.selector)

        t_start = time.time()
        try:
            solution = solver.solve(formula)
            t_end = time.time()
            print(solver._n_calls, t_end - t_start)
        except TimeoutException:
            solution = None
            print("(aborted)")
            return None
        if solution is not None:
            assert formula.evaluate(solution)

        return Result(
            result=solution is not None,
            runtime=t_end - t_start,
            n_calls=solver._n_calls
        )

    def _write_results(
        self, results: List[Result], l: int, dataset_config: Dict, outpath: str
    ):

        results_json = {
            "dataset": dataset_config,
            "l": l,
            "results": [
                asdict(result) for result in results if result is not None
            ]
        }

        if not os.path.exists(outpath):
            os.makedirs(outpath)

        with open(os.path.join(outpath, f"l={l}.json"), "w") as f:
            json.dump(results_json, f)

        return
