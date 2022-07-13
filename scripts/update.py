import pandas as pd
from pathlib import Path

FILEPATH_DIR = Path(__file__).parent


def main():
    df = pd.read_csv(f"{FILEPATH_DIR.parent}/build/data.csv")

    # Add the column slug if it doesn't exist
    if "slug" not in df.columns:
        df["slug"] = df.display_name.str.lower().str.replace(" ", "-")
        # If there are duplicates, add a number to the end
        df["slug"] = df.slug.apply(
            lambda x: x + "-" + str(df[df.slug == x].index.values[0] + 1)
            if df[df.slug == x].shape[0] > 1
            else x
        )

    # Write to csv
    df.to_csv(f"{FILEPATH_DIR.parent}/build/data.csv", index=False)

if __name__ == "__main__":
    main()
    print("Done!")
    exit(0)