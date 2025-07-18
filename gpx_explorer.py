import os
import pathlib
import random
import re
import sys
from datetime import datetime

import cartopy.crs as ccrs
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors


def parse_gpx_to_dataframe(file) -> pd.DataFrame:
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
                        time_list.append(point.time),
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


def plot_track(df):
    """Takes a dataframe and visualises it with a matplotlib chart"""

    # fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator())

    ax.scatter(
        df.longitude,
        df.latitude,
        transform=ccrs.PlateCarree(),
        s=df.hdop,
        alpha=[min(1 / i, 1) for i in df.hdop],
    )

    plt.title("GPX Tracks")
    plt.show()


def combine_tracks(folder) -> pd.DataFrame:
    """Takes a folder as input and returns all gpx files combined into a single dataframe"""
    combined_df = pd.DataFrame()

    for track_file in pathlib.Path("tracks").iterdir():
        if track_file.is_file():
            track_df = parse_gpx_to_dataframe(track_file)
        combined_df = (
            pd.concat([combined_df, track_df]).reset_index().drop("index", axis=1)
        )
    return combined_df


def choose_random_track(folder):
    """Takes a folder path as input and returns a random file path from within that folder"""
    file_list = []

    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path):
            file_list.append(f)

    random_track = random.choice(file_list)
    random_track_full_path = os.path.join(folder, random_track)

    return random_track_full_path


if __name__ == "__main__":
    gpx_tracks_folder = "tracks"

    if not os.path.isfile(gpx_tracks_folder):
        sys.exit("Tracks folder not found!")

    # combine_tracks(gpx_tracks_folder)
    # choose_random_track(gpx_tracks_folder)
    random_gpx_file = choose_random_track(gpx_tracks_folder)
    df_random_track = parse_gpx_to_dataframe(random_gpx_file)

    regex_match = re.search(r"tracks\\(.+)\.gpx", random_gpx_file)

    if regex_match:
        random_gpx_file_name = regex_match.group(1)
    else:
        random_gpx_file_name = "No Filename"

    with open(random_gpx_file) as f:
        random_gpx_track = gpxpy.parse(f)

    csv_path = "combined_gpx_tracks.csv"

    if os.path.isfile(csv_path):
        df_combined = pd.read_csv(csv_path)
    else:
        df_combined = combine_tracks(gpx_tracks_folder)
        df_combined.to_csv(csv_path)

    for df in (df_random_track, df_combined):
        df["time"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert(None)

    stats = {
        "Max Speed": df_random_track["speed"].max(),
        "Length (km)": random_gpx_track.length_3d() / 1000,
        "Duration": max(df_random_track["time"]) - min(df_random_track["time"]),
    }
    random_gpx_track_top_speed = df_random_track["speed"].idxmax()

    random_gpx_track_top_speed_longitude = df_random_track.at[
        random_gpx_track_top_speed, "longitude"
    ]
    random_gpx_track_top_speed_latitude = df_random_track.at[
        random_gpx_track_top_speed, "latitude"
    ]

    random_gpx_track_top_height = df_random_track["height"].idxmax()

    random_gpx_track_top_height_longitude = df_random_track.at[
        random_gpx_track_top_height, "longitude"
    ]
    random_gpx_track_top_height_latitude = df_random_track.at[
        random_gpx_track_top_height, "latitude"
    ]

    fig = plt.figure(figsize=(16, 9))

    gs = fig.add_gridspec(2, 3)

    ax0 = fig.add_subplot(gs[0, 2])
    ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.Mercator())
    ax2 = fig.add_subplot(gs[0, 1], projection=ccrs.Mercator())
    ax3 = fig.add_subplot(gs[1, :])

    fig.suptitle("GPS tracks overview")

    ax0.set_title("Speed Histogram")
    ax0.set_xlabel("Meters per Second")

    df_random_track["speed"].hist(ax=ax0, bins=50)

    for ax in (ax1, ax2):
        gl = ax.gridlines(
            draw_labels=True, crs=ccrs.PlateCarree(), linestyle="--", alpha=0.4
        )
        gl.top_labels = False
        gl.right_labels = False

    ax1.set_title("Combined GPS tracks")
    ax1.scatter(
        df_combined.longitude,
        df_combined.latitude,
        s=df_combined.hdop,
        alpha=[min(1 / i, 1) for i in df_combined.hdop],
        transform=ccrs.PlateCarree(),
    )
    ax1.plot(
        df_random_track.longitude,
        df_random_track.latitude,
        color="red",
        transform=ccrs.PlateCarree(),
    )

    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")

    ax2.set_title(random_gpx_file_name)
    cmap = plt.get_cmap("inferno")
    norm = plt.Normalize(df_random_track.speed.min(), df_random_track.speed.max())
    point_colours = cmap(norm(df_random_track.speed))

    ax2.scatter(
        df_random_track.longitude,
        df_random_track.latitude,
        transform=ccrs.PlateCarree(),
        s=1,
        c=df_random_track["speed"],
        cmap="turbo",
        norm=colors.LogNorm(
            df_random_track["speed"].min(), df_random_track["speed"].max()
        ),
    )

    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")

    ax2.annotate(
        "Top speed",
        xy=(random_gpx_track_top_speed_longitude, random_gpx_track_top_speed_latitude),
        xycoords=ccrs.PlateCarree(),
        xytext=(20, 20),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="red", lw=1),
        fontsize=12,
        color="red",
    )
    ax2.annotate(
        "Highest Point",
        xy=(
            random_gpx_track_top_height_longitude,
            random_gpx_track_top_height_latitude,
        ),
        xycoords=ccrs.PlateCarree(),
        xytext=(20, 20),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="red", lw=1),
        fontsize=12,
        color="red",
    )

    ax3.plot(df_random_track.time, df_random_track.height, c="red", label="Height(m)")
    ax3.plot(df_random_track.time, df_random_track.speed, c="green", label="Speed(m/s)")
    ax3.plot(
        df_random_track.time,
        df_random_track.hdop,
        c="blue",
        label="GPS h/v dop",
        linestyle="dotted",
    )

    ax3.legend(
        loc="best", frameon=True, fancybox=True, framealpha=0.9, title="Measurements"
    )

    ax3.set_xlabel("Time")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "Results")
    file_name = datetime.now().strftime("%Y-%m-%d - %H-%M-%S") + ".png"
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    file_path = os.path.join(results_dir, file_name)
    plt.savefig(file_path)
    plt.show()
