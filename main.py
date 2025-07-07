import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import re
import cartopy.crs as ccrs
import pathlib
import gpxpy
import random
import os


def get_lon_lat_lists(file):
    longitude_list = []
    latitude_list = []
    with open(file) as gpx_file:

        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    longitude_list.append(point.longitude), latitude_list.append(
                        point.latitude
                    )

        return longitude_list, latitude_list


def plot_track(longitude_list, latitude_list):

    fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator())

    ax.scatter(longitude_list, latitude_list, transform=ccrs.PlateCarree(), s=1)

    plt.title(f"GPX Tracks")
    plt.show()


def combine_tracks(folder):
    complete_longitudes = []
    complete_latitudes = []

    for track_file in pathlib.Path("tracks").iterdir():
        if track_file.is_file():
            longitude_list, latitude_list = get_lon_lat_lists(track_file)
            complete_longitudes.extend(longitude_list)
            complete_latitudes.extend(latitude_list)
    return complete_longitudes, complete_latitudes


def choose_random_track(folder):

    file_list = []

    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path):
            file_list.append(f)

    random_track = random.choice(file_list)
    random_track_full_path = os.path.join(folder, random_track)

    longitude_list = []
    latitude_list = []

    longitude_list, latitude_list = get_lon_lat_lists(random_track_full_path)

    return longitude_list, latitude_list


if __name__ == "__main__":
    gpx_tracks_folder = "tracks"
    # combine_tracks(gpx_tracks_folder)
    # choose_random_track(gpx_tracks_folder)
    plot_track(*choose_random_track(gpx_tracks_folder))
    # plot_track(combine_tracks(gpx_tracks_folder))
