import pandas as pd
from pathlib import Path

FILEPATH_DIR = Path(__file__).parent


def main():
    df = pd.read_csv(f"{FILEPATH_DIR.parent}/build/data.csv")

    # Add the columns display_name and slug
    series_fmtd = df["series"].apply(lambda x: str(x) + " " if not pd.isnull(x) else "")
    df["display_name"] = (df.make + " " + series_fmtd + df.model).str.strip()
    df["display_name"] = df.display_name.str.replace(r"\s+", " ").str.title()

    # Remove duplicates if display_name (case insensitive) is the same
    df["display_name_lower"] = df["display_name"].str.lower()
    df = df.drop_duplicates(subset=["display_name_lower"])
    df = df.drop(columns=["display_name_lower"])

    df["slug"] = (
        (df.make + "+" + series_fmtd + df.model).str.lower().str.replace(" ", "-")
    )

    # If there are duplicates, add a number to the end
    df["slug"] = df.slug.apply(
        lambda x: x + "_" + str(df[df.slug == x].reset_index().index.values[0] + 1)
        if df[df.slug == x].shape[0] > 1
        else x
    )

    # Write to csv
    df.to_csv(f"{FILEPATH_DIR.parent}/build/data.csv", index=False)


if __name__ == "__main__":
    main()
    print("Done!")
    exit(0)
