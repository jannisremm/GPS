from __future__ import annotations

import argparse
import sys
from pathlib import Path

import gpxpy
import pandas as pd

from .core import (
    choose_random_track,
    combine_tracks,
    parse_gpx_to_dataframe,
)
from .plotting import plot_overview, plot_track


def main() -> None:
    p = argparse.ArgumentParser(
        prog="gpx-explorer",
        description="Analyse and visualise GPX tracks.",
    )
    p.add_argument(
        "target",
        type=Path,
        help="A .gpx file or a directory containing .gpx files.",
    )
    p.add_argument(
        "--overview",
        action="store_true",
        help="Generate the full multi-panel overview PNG.",
    )
    p.add_argument(
        "-f",
        "--force_csv",
        action="store_true",
        help="Recreate 'combined_gpx_tracks.csv' even if it already exists.",
    )

    ns = p.parse_args()

    if ns.target.is_file():
        df = parse_gpx_to_dataframe(ns.target)
        if ns.overview:
            with ns.target.open() as f:
                gpx_obj = gpxpy.parse(f)
            plot_overview(df, df, gpx_obj)
        else:
            plot_track(df)

    elif ns.target.is_dir():
        csv_path = Path("combined_gpx_tracks.csv")
        if ns.force_csv or not csv_path.is_file():
            df_combined = combine_tracks(ns.target)
            df_combined.to_csv(csv_path, index=False)
        else:
            df_combined = pd.read_csv(csv_path)

        random_file = choose_random_track(ns.target)
        df_random = parse_gpx_to_dataframe(random_file)
        if ns.overview:
            with random_file.open() as f:
                gpx_obj = gpxpy.parse(f)
            plot_overview(df_random, df_combined, gpx_obj)
        else:
            plot_track(df_combined)
    else:
        sys.exit(f"{ns.target} is neither file nor directory")


if __name__ == "__main__":
    main()
