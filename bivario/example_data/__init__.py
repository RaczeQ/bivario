"""Example datasets for bivario package."""

from pathlib import Path

import geopandas as gpd

__all__ = ["nyc_bike_trips"]


def nyc_bike_trips() -> gpd.GeoDataFrame:
    """
    Load example NYC bike trips data as a GeoDataFrame.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing NYC bike trips data.
    """
    data_path = Path(__file__).parent / "nyc_bike_trips.parquet"
    gdf = gpd.read_parquet(data_path).set_index("h3")
    return gdf
