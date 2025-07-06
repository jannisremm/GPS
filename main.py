import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import re


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
                coordinate.attrib.get("lat"),
                coordinate.attrib.get("lon"),
            )
        )
        latitude_list.append(float(coordinate.attrib.get("lat")))
        longitude_list.append(float(coordinate.attrib.get("lon")))

    return longitude_list, latitude_list


if __name__ == "__main__":

    tree = ET.parse("test.gpx")
    root = tree.getroot()

    x, y = get_lon_lat_lists(root)

    plt.plot(x, y)
    plt.show()
