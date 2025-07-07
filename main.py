import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import re
import cartopy.crs as ccrs
import pathlib
import gpxpy


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


if __name__ == "__main__":
    complete_longitudes = []
    complete_latitudes = []

    for track_file in pathlib.Path("tracks").iterdir():
        if track_file.is_file():
            longitude_list, latitude_list = get_lon_lat_lists(track_file)
            complete_longitudes.extend(longitude_list)
            complete_latitudes.extend(latitude_list)
            #  plot_track(longitude_list, latitude_list)
    plot_track(complete_longitudes, complete_latitudes)
