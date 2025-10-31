"""Fixtures for tests."""

import geopandas as gpd
import pytest

from bivario.example_data import nyc_bike_trips


@pytest.fixture  # type: ignore
def dummy_data() -> gpd.GeoDataFrame:
    """Example geodataframe."""
    return gpd.GeoDataFrame(
        dict(a=[1, 2], b=[10, 100]), geometry=gpd.GeoSeries.from_xy([0, 1], [1, 1], crs=4326)
    )


@pytest.fixture  # type: ignore
def nyc_data() -> gpd.GeoDataFrame:
    """Example real dataset geodataframe."""
    return nyc_bike_trips()
