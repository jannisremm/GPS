from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import cartopy.crs as ccrs
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd

from .core import (
    get_track_extremes,
)

__all__ = ["plot_track", "plot_overview"]


def plot_track(df: pd.DataFrame) -> None:
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


def plot_overview(
    df_single_track: pd.DataFrame,
    df_all_tracks: pd.DataFrame,
    gpx_obj: gpxpy.gpx.GPX,
    outfile_dir: Path | str = "Results",
) -> Path:
    """creates an overview plot from df_all_tracks, and detail views from df_single_track"""
    fig = plt.figure(figsize=(18, 12))

    gs = fig.add_gridspec(3, 3)

    # Single track histogram
    ax0 = fig.add_subplot(gs[0, 2])
    # Combined tracks overview
    ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.Mercator())
    # Single track detail view
    ax2 = fig.add_subplot(gs[0, 1], projection=ccrs.Mercator())
    # Single track speed / height / hdop vs time
    ax3 = fig.add_subplot(gs[1, :])
    # Single track speed / height vs distance
    ax4 = fig.add_subplot(gs[2, :])

    fig.suptitle("GPS tracks overview")

    ax0.set_title("Speed Histogram")
    ax0.set_xlabel("Kilometers per Hour")

    df_single_track["speed"].hist(ax=ax0, bins=50, log=True)

    ax0.set_yscale("log")
    ax0.set_ylim(0, None) # Shows a warning  in the console, but otherwise values of 1 wouldn't show

    ax0.yaxis.set_major_locator(mticker.LogLocator(base=10))
    ax0.yaxis.set_minor_locator(
        mticker.LogLocator(base=10, subs=(1, 2, 3, 4, 5, 6, 7, 8, 9))
    )

    ax0.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda y, _: "{:.16g}".format(y))
    )

    ax0.yaxis.set_minor_formatter(mticker.NullFormatter())

    ax0.set_ylabel("Count (log scale)")

    for ax in (ax1, ax2):
        gl = ax.gridlines(
            draw_labels=True, crs=ccrs.PlateCarree(), linestyle="--", alpha=0.4
        )
        gl.top_labels = False
        gl.right_labels = False

    ax1.set_title("Combined GPS tracks")

    # Unfinished implementation of map extents auto-adjustment
    # all_tracks_longitude_stddev = df_all_tracks["longitude"].std() * 0.5
    # all_tracks_longitude_mean = df_all_tracks["longitude"].mean()
    # all_tracks_latitude_stddev = df_all_tracks["latitude"].std() * 0.5
    # all_tracks_latitude_mean = df_all_tracks["latitude"].mean()

    # ax1.set_extent(
    #     (
    #         (all_tracks_longitude_mean - all_tracks_longitude_stddev),
    #         (all_tracks_longitude_mean + all_tracks_longitude_stddev),
    #         (all_tracks_latitude_mean - all_tracks_latitude_stddev),
    #         (all_tracks_latitude_mean + all_tracks_latitude_stddev),
    #     ),
    #     crs=ccrs.PlateCarree(),
    # )

    ax1.set_extent((9.85, 10.15, 53.5, 53.65))

    ax1.scatter(
        df_all_tracks.longitude,
        df_all_tracks.latitude,
        s=df_all_tracks.hdop,
        alpha=[min(1 / i, 1) for i in df_all_tracks.hdop],
        transform=ccrs.PlateCarree(),
    )
    ax1.plot(
        df_single_track.longitude,
        df_single_track.latitude,
        color="red",
        transform=ccrs.PlateCarree(),
    )

    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")

    ax2.set_title("Randomly selected track")

    speed_chart = ax2.scatter(
        df_single_track.longitude,
        df_single_track.latitude,
        transform=ccrs.PlateCarree(),
        s=1,
        c=df_single_track["speed"],
        cmap="turbo",
        # norm=colors.LogNorm(
        #     df_single_track["speed"].min(), df_single_track["speed"].max()
        # ),
    )

    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")

    ax2.set_box_aspect(1)

    fig.colorbar(
        speed_chart,
        ax=ax2,
        label="Speed (km/h)",
        location="right",
        shrink=0.7,
    )

    speed_idx, height_idx = get_track_extremes(df_single_track)

    single_track_top_speed_longitude = df_single_track.at[speed_idx, "longitude"]
    single_track_top_speed_latitude = df_single_track.at[speed_idx, "latitude"]
    single_track_top_height_longitude = df_single_track.at[height_idx, "longitude"]
    single_track_top_height_latitude = df_single_track.at[height_idx, "latitude"]

    ax2.annotate(
        f"Top speed {df_single_track['speed'].max():.1f} km/h",
        xy=(single_track_top_speed_longitude, single_track_top_speed_latitude),
        xycoords=ccrs.PlateCarree(),
        xytext=(20, 20),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="red", lw=1),
        fontsize=12,
        color="red",
    )
    ax2.annotate(
        f"Highest Point {df_single_track['height'].max():.1f} m",
        xy=(
            single_track_top_height_longitude,
            single_track_top_height_latitude,
        ),
        xycoords=ccrs.PlateCarree(),
        xytext=(20, 20),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="red", lw=1),
        fontsize=12,
        color="red",
    )

    fig.colorbar(
        speed_chart,
        ax=ax2,
        label="Speed (km/h)",
        location="bottom",
        shrink=0.7,
        # norm=colors.Normalize(vmin=0, vmax=df_single_track["speed"].max()),
    )

    ax3.plot(df_single_track.time, df_single_track.height, c="red", label="Height(m)")
    ax3.plot(
        df_single_track.time, df_single_track.speed, c="green", label="Speed(km/h)"
    )
    ax3.plot(
        df_single_track.time,
        df_single_track.hdop,
        c="blue",
        label="GPS h/v dop",
        linestyle="dotted",
    )

    ax3.legend(
        loc="best", frameon=True, fancybox=True, framealpha=0.9, title="Measurements"
    )

    ax3.set_xlabel("Time")

    ax4.plot(
        df_single_track.distance, df_single_track.speed, c="green", label="Speed(km/s)"
    )
    ax4.plot(
        df_single_track.distance, df_single_track.height, c="red", label="Height(m)"
    )

    ax4.set_xlabel("Distance (km)")

    results_dir = Path(outfile_dir).expanduser().resolve()
    file_name = datetime.now().strftime("%Y-%m-%d - %H-%M-%S") + ".png"
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    file_path = os.path.join(results_dir, file_name)
    plt.savefig(file_path)
    plt.show()

    return file_path
