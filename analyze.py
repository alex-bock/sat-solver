
import argparse
import glob
import json
import os
import pandas as pd


def parse_cli() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("--method")
    parser.add_argument("-n", type=int)

    return parser.parse_args()


if __name__ == "__main__":

    cli_args = parse_cli()
    method = cli_args.method

    for fp in sorted(glob.glob(os.path.join("results", method, f"n={cli_args.n}", "l=*.json"))):
        with open(fp, "r") as f:
            result_json = json.load(f)
        print("l =", result_json["l"], f"({len(result_json['results'])} iter.)")
        if len(result_json["results"]) == 0:
            continue
        results_df = pd.DataFrame(result_json["results"])
        sat_rate = len(results_df[results_df.result]) / 100
        print(f"- sat. rate:       {round(sat_rate * 100, 2)}%")
        print(f"- med. runtime:    {round(results_df.runtime.median(), 2)}s")
        print(f"- med. call count: {int(results_df.n_calls.median())}")
