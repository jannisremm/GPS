import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import re
import cartopy.crs as ccrs
import pathlib


def get_lon_lat_lists(root):
    """Takes an xml tree and outputs a list of longitude and latitude"""

    # Find the correct namespace for the gpx file
    namespace_search = re.search(r"\{(.*?)\}", root.tag)
    if namespace_search:
        namespace = namespace_search.group(1)

    latitude_list = []
    longitude_list = []
    coordinates_list = []

    for coordinate in root.iter(f"{{{namespace}}}trkpt"):
        coordinates_list.append(
            (
                float(coordinate.attrib.get("lat")),
                float(coordinate.attrib.get("lon")),
            )
        )
        latitude_list.append(float(coordinate.attrib.get("lat")))
        longitude_list.append(float(coordinate.attrib.get("lon")))

    return longitude_list, latitude_list, coordinates_list


def plot_track(track_file):
    print(track_file.name)

    tree = ET.parse(f"{track_file}")
    root = tree.getroot()

    longitude_list, latitude_list, coordinates_list = get_lon_lat_lists(root)

    fig = plt.figure()
    ax = plt.axes(projection=ccrs.Mercator())

    ax.scatter(longitude_list, latitude_list, transform=ccrs.PlateCarree(), s=1)

    plt.title(f"GPX Tracks {track_file.name}")
    plt.show()


if __name__ == "__main__":

    for track_file in pathlib.Path("tracks").iterdir():
        if track_file.is_file():
            plot_track(track_file)
