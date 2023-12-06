
import argparse

from sat.experiment import Experiment
from sat.selectors import (
    NaiveSelector,
    RandomChoiceSelector,
    TwoClauseSelector,
    ModalVariableSelector
)


SELECTORS = {
    "naive": NaiveSelector,
    "random": RandomChoiceSelector,
    "two": TwoClauseSelector,
    "modal": ModalVariableSelector
}


def parse_cli() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("--method")
    parser.add_argument("-n", dest="n_vars", type=int)
    parser.add_argument("-rmin", dest="min_ratio", type=float, default=3.0)
    parser.add_argument("-rmax", dest="max_ratio", type=float, default=6.0)
    parser.add_argument("-rstep", dest="ratio_step", type=float, default=0.2)

    return parser.parse_args()


if __name__ == "__main__":

    cli_args = parse_cli()

    exp = Experiment(
        selector=SELECTORS[cli_args.method](),
        n_vars=cli_args.n_vars,
        min_ratio=cli_args.min_ratio,
        max_ratio=cli_args.max_ratio,
        ratio_step=cli_args.ratio_step
    )
    exp.run(f"results/{cli_args.method}/")
