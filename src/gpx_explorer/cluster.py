from pathlib import Path

import hdbscan
import matplotlib.pyplot as plt
import seaborn as sns

from .core import choose_random_track, parse_gpx_to_dataframe

tracks_directory = Path("tracks")

random_track = choose_random_track(tracks_directory)
print(random_track)

random_track_dataframe = parse_gpx_to_dataframe(random_track)
coordinates_df = random_track_dataframe[["latitude", "longitude"]]

clusterer = hdbscan.HDBSCAN(
    algorithm="best",
    alpha=0.8,
    metric="euclidean",
    min_cluster_size=15,
)


def cluster_gps_points(dataframe):
    clusterer.fit(dataframe)

    # print(clusterer.labels_)

    print(f"Number of clusters: {clusterer.labels_.max() + 1}")

    # print(clusterer.probabilities_)

    return 0


cluster_gps_points(coordinates_df)

# plt.scatter(
#     coordinates_df["longitude"],
#     coordinates_df["latitude"],
#     s=50,
#     linewidth=0,
#     c="b",
#     alpha=0.25,
# )
# plt.show()

color_palette = sns.color_palette("deep", 8)
cluster_colors = [
    color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in clusterer.labels_
]
cluster_member_colors = [
    sns.desaturate(x, p) for x, p in zip(cluster_colors, clusterer.probabilities_)
]
plt.scatter(
    coordinates_df["longitude"],
    coordinates_df["latitude"],
    s=50,
    linewidth=0,
    c=cluster_member_colors,
    alpha=0.25,
)
plt.show()
