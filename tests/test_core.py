from __future__ import annotations

import pandas as pd

from gpx_explorer.core import (
    get_track_extremes,
)


def test_get_track_extremes() -> None:
    """Indices of maximum speed and height should be returned."""

    df = pd.DataFrame({"speed": [1, 5, 2, 3], "height": [5, 1, 10, 3]})

    idx_speed, idx_height = get_track_extremes(df)

    assert idx_speed == 1
    assert idx_height == 2
