
from sat.experiment import Experiment
from sat.selectors import (
    NaiveSelector,
    RandomChoiceSelector,
    TwoClauseSelector
)


if __name__ == "__main__":

    exp = Experiment(selector=RandomChoiceSelector(), n_vars=100, min_ratio=3.0, max_ratio=6.0, ratio_step=0.2)
    exp.run("results/random/", n_iter=10)
