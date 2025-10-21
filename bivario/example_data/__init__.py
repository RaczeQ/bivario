"""Example datasets for bivario package."""

from pathlib import Path

import geopandas as gpd

__all__ = ["nyc_bike_trips"]


def nyc_bike_trips() -> gpd.GeoDataFrame:
    """
    Load example NYC bike trips data as a GeoDataFrame.

    Contains H3-indexed bike trip start and end locations in New York City.
    Starts and split into morning and afternoon trips.

    Available columns:
        - h3: H3 index of the location
        - morning_starts: Number of bike trips starting in the morning
        - morning_ends: Number of bike trips ending in the morning
        - afternoon_starts: Number of bike trips starting in the afternoon
        - afternoon_ends: Number of bike trips ending in the afternoon
        - geometry: Geometry of the H3 cell

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing NYC bike trips data.

    Examples:
        Plot example folium map with this data:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import explore_bivariate_data
        >>> explore_bivariate_data(
        ...     nyc_bike_trips(),
        ...     column_a="morning_starts",
        ...     column_b="morning_ends",
        ... )
        <folium.folium.Map object at 0x...>
    """
    data_path = Path(__file__).parent / "nyc_bike_trips.csv.gz"
    df = gpd.pd.read_csv(data_path)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["geometry"], crs=4326))
    return gdf
