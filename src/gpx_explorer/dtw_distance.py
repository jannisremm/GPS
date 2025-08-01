import glob
import pathlib
from pathlib import Path

import numpy as np
from dtw import dtw

from .core import parse_gpx_to_dataframe

tracks_folder = Path("tracks")
gpx_files = glob.glob("tracks/*.gpx")

gpx_files.sort()


def get_track_data(path: str | pathlib.Path):
    df = parse_gpx_to_dataframe(path)
    return np.array(df[["latitude", "longitude"]])


tracks = [get_track_data(file) for file in gpx_files[100:120]]


dtw_distances = np.zeros((len(tracks), len(tracks)))


for i in range(len(tracks)):
    for j in range(i + 1, len(tracks)):
        print(f"PROCESSING {i}-{j}")

        track_1 = tracks[i]
        track_2 = tracks[j]

        distance = dtw(track_1, track_2).distance

        dtw_distances[i, j] = distance
        dtw_distances[j, i] = distance


np.save("dtw_distances.npy", dtw_distances)

print(dtw_distances)
