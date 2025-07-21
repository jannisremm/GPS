from importlib.metadata import PackageNotFoundError, version

from .core import (
    choose_random_track,
    combine_tracks,
    parse_gpx_to_dataframe,
)
from .plotting import plot_track

__all__ = [
    "parse_gpx_to_dataframe",
    "combine_tracks",
    "choose_random_track",
    "plot_track",
    "__version__",
]

try:
    __version__ = version(__package__ or "gpx-explorer")
except PackageNotFoundError:
    __version__ = "0.0.0"
