# This script was used to bootstrap this repo. It is not used anymore.

import pandas as pd
from pathlib import Path
import json

FILPATH_DIR = Path(__file__).parent


def main():

    # Read in the data
    with open(f"{FILPATH_DIR.parent}/models.json", "r") as f:
        data_j_raw = json.load(f)
    # Convert to pandas dataframe
    data_j = []
    for instance in data_j_raw:
        make = instance["name"]
        for model in instance["models"]:
            data_j.append({"make": make, **model})

    data_c = pd.read_csv(f"{FILPATH_DIR.parent}/models.csv")
    data_j = pd.DataFrame(data_j)

    # Let's normalize the columns
    data_c["series"] = None
    data_j.columns = ["make", "model", "series"]

    # Merge the dataframes
    df = pd.concat([data_c, data_j], ignore_index=True)

    # Add the column "available_in_IT"
    df["available_in_IT"] = True  # For now

    # Delete duplicates
    df = df.drop_duplicates(subset=["model", "series"])

    # Add the column "display_name"
    series_fmtd = df["series"].apply(lambda x: x + " " if x else "")
    df["display_name"] = (
        df["make"] + " " + series_fmtd + df["model"]
    )  # Watch out fot the spaces

    # Write to csv
    df.to_csv("build/models.csv", index=False)


if __name__ == "__main__":
    main()
