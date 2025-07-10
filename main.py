import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pathlib
import gpxpy
import random
import os
import pandas as pd


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
                for point in segment.points:
                    longitude_list.append(point.longitude), latitude_list.append(
                        point.latitude
                    ), height_list.append(point.elevation), speed_list.append(
                        point.speed
                    ), hdop_list.append(
                        point.horizontal_dilution
                    ), time_list.append(
                        point.time
                    )

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

    fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator())

    ax.scatter(
        df.longitude,
        df.latitude,
        transform=ccrs.PlateCarree(),
        s=df.hdop,
        alpha=[min(1 / i, 1) for i in df.hdop],
    )

    plt.title(f"GPX Tracks")
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


# def track_infos(track)


if __name__ == "__main__":
    gpx_tracks_folder = "tracks"
    # combine_tracks(gpx_tracks_folder)
    # choose_random_track(gpx_tracks_folder)
    random_track = choose_random_track(gpx_tracks_folder)
    df_random_track = parse_gpx_to_dataframe(random_track)

    # plot_track(lon, lat, hdop)

    df_combined = combine_tracks(gpx_tracks_folder)

    plot_track(df_random_track)
    plot_track(df_combined)
