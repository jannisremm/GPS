from __future__ import annotations

import os
import pathlib
import random
from pathlib import Path
from typing import Tuple

import gpxpy
import pandas as pd

__all__ = [
    "parse_gpx_to_dataframe",
    "combine_tracks",
    "choose_random_track",
    "compute_track_stats",
    "get_track_extremes",
]


def parse_gpx_to_dataframe(file: str | pathlib.Path) -> pd.DataFrame:
    """Takes a gpx file and uses gpxpy to transform it into a pandas dataframe"""

    longitude_list = []
    latitude_list = []
    height_list = []
    speed_list = []
    hdop_list = []
    time_list = []
    with open(file) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                previous_point = None
                for point in segment.points:
                    if previous_point and point.time and previous_point.time:
                        speed = max(point.speed_between(previous_point), 0.001)
                    else:
                        speed = 0.001

                    (
                        longitude_list.append(point.longitude),
                        latitude_list.append(point.latitude),
                        height_list.append(point.elevation),
                        speed_list.append(speed),
                        hdop_list.append(point.horizontal_dilution),
                        time_list.append(pd.to_datetime(str(point.time), utc=True)),
                    )
                    previous_point = point

        gpx_dict = {
            "longitude": longitude_list,
            "latitude": latitude_list,
            "height": height_list,
            "speed": speed_list,
            "hdop": hdop_list,
            "time": time_list,
        }

        df = pd.DataFrame(gpx_dict)

        return df


def combine_tracks(folder: str | pathlib.Path) -> pd.DataFrame:
    """Takes a folder as input and returns all gpx files combined into a single dataframe"""
    combined_df = pd.DataFrame()

    for track_file in pathlib.Path(folder).glob("*.gpx"):
        if track_file.is_file():
            track_df = parse_gpx_to_dataframe(track_file)
            combined_df = (
                pd.concat([combined_df, track_df]).reset_index().drop("index", axis=1)
            )
    return combined_df


def choose_random_track(folder: str | Path) -> Path:
    """Takes a folder path as input and returns a the path of a random .gpx file from within that folder"""
    file_list = []

    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path):
            if f.endswith(".gpx"):
                file_list.append(f)

    if not file_list:
        raise FileNotFoundError(f"No GPX files found in {folder}")

    random_track = random.choice(file_list)

    return Path(folder) / random_track


def compute_track_stats(df: pd.DataFrame, gpx_obj: gpxpy.gpx.GPX) -> dict[str, object]:
    """Return dict with max speed, length (km) and duration."""
    return {
        "max_speed": df["speed"].max(),
        "length_km": gpx_obj.length_3d() / 1_000,
        "duration": df["time"].max() - df["time"].min(),
    }


def get_track_extremes(df: pd.DataFrame) -> Tuple[int, int]:
    """Return row-indices of top speed and top height."""
    return df["speed"].idxmax(), df["height"].idxmax()
