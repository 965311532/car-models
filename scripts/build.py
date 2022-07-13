import pandas as pd
from pathlib import Path
import simplejson

FILPATH_DIR = Path(__file__).parent

def main():
    df = pd.read_csv(f"{FILPATH_DIR.parent}/build/data.csv")
    
    # Create a json file with the data ordered by make
    j = df.groupby("make").apply(lambda x: x.to_dict("records")).to_dict()

    with open(f"{FILPATH_DIR.parent}/dist.json", "w") as f:
        simplejson.dump(j, f, ignore_nan=True)

if __name__ == "__main__":
    main()