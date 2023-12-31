
import argparse
import json

from sat.puzzle import Puzzle
from sat.solvers import DPLL

from sat.selectors import (
    NaiveSelector,
    RandomChoiceSelector,
    TwoClauseSelector
)


SELECTORS = {
    "naive": NaiveSelector,
    "rand": RandomChoiceSelector,
    "two": TwoClauseSelector
}


def parse_cli() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--selector",
        default="naive"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true"
    )

    return parser.parse_args()


def build_puzzle() -> Puzzle:

    puzzle = Puzzle(
        n=5,
        vals={
            "cig": ["ble", "blu", "dun", "pal", "pri"],
            "col": ["blu", "gre", "red", "whi", "yel"],
            "dri": ["bee", "cof", "mil", "tea", "wat"],
            "nat": ["bri", "dan", "ger", "nor", "swe"],
            "pet": ["bir", "cat", "dog", "fis", "hor"]
        }
    )

    puzzle.location("dri", "mil", 2)
    puzzle.location("nat", "nor", 0)

    puzzle.coincidence("nat", "bri", "col", "red")
    puzzle.coincidence("nat", "swe", "pet", "dog")
    puzzle.coincidence("nat", "dan", "dri", "tea")
    puzzle.coincidence("col", "gre", "dri", "cof")
    puzzle.coincidence("cig", "pal", "pet", "bir")
    puzzle.coincidence("col", "yel", "cig", "dun")
    puzzle.coincidence("cig", "blu", "dri", "bee")
    puzzle.coincidence("nat", "ger", "cig", "pri")

    puzzle.adjacent("cig", "ble", "pet", "cat")
    puzzle.adjacent("pet", "hor", "cig", "dun")
    puzzle.adjacent("nat", "nor", "col", "blu")
    puzzle.adjacent("cig", "ble", "dri", "wat")

    puzzle.consecutive("col", "gre", "col", "whi")

    return puzzle


if __name__ == "__main__":

    cli_args = parse_cli()
    puzzle = build_puzzle()

    puzzle_cnf = puzzle.cnf
    puzzle_cnf.to_dimacs("./output/dimacs.txt")
    with open("./output/cnf.txt", "w") as f:
        for clause in puzzle_cnf:
            f.write(str(clause) + "\n")
    with open("./output/var_map.json", "w") as f:
        json.dump(puzzle_cnf._var_map, f)

    solver = DPLL(
        selector=SELECTORS[cli_args.selector](),
        verbose=cli_args.verbose
    )
    tau = solver.solve(puzzle_cnf)
    with open("./output/solution.txt", "w") as f:
        for (var, val) in tau.items():
            if val:
                f.write(str(puzzle_cnf._var_map[var]) + " " +  var + "\n")
    print(tau)
    print(puzzle_cnf.evaluate(tau))
