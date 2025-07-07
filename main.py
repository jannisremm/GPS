import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pathlib
import gpxpy
import random
import os


def convert_to_lists(file):
    longitude_list = []
    latitude_list = []
    height_list = []
    speed_list = []
    hdop_list = []
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
                    )

        return longitude_list, latitude_list, height_list, speed_list, hdop_list


def plot_track(longitude_list, latitude_list, hdop_list, alpha_list):

    fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator())

    ax.scatter(
        longitude_list,
        latitude_list,
        transform=ccrs.PlateCarree(),
        s=hdop_list,
        alpha=alpha_list,
    )

    plt.title(f"GPX Tracks")
    plt.show()


def combine_tracks(folder):
    complete_longitudes = []
    complete_latitudes = []
    complete_hdop = []

    for track_file in pathlib.Path("tracks").iterdir():
        if track_file.is_file():
            longitude_list, latitude_list, height, speed, hdop = convert_to_lists(
                track_file
            )
            complete_longitudes.extend(longitude_list)
            complete_latitudes.extend(latitude_list)
            complete_hdop.extend(hdop)
    return complete_longitudes, complete_latitudes, complete_hdop


def choose_random_track(folder):

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
    # random_track = choose_random_track(gpx_tracks_folder)
    # lon, lat, height, speed, hdop = convert_to_lists(random_track)

    # plot_track(lon, lat, hdop)

    lon, lat, hdop = combine_tracks(gpx_tracks_folder)
    talpha = [min(1 / i, 1) for i in hdop]

    plot_track(lon, lat, hdop, talpha)
