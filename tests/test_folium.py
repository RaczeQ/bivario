"""Test folium plotting functionality."""

import folium
import geopandas as gpd


def test_explore_bivariate_data() -> None:
    """Test that explore_bivariate_data can be run without error."""
    from bivario import explore_bivariate_data

    m = explore_bivariate_data(
        gpd.GeoDataFrame(
            dict(a=[1, 2], b=[10, 100]), geometry=gpd.GeoSeries.from_xy([0, 1], [1, 1], crs=4326)
        ),
        column_a="a",
        column_b="b",
    )

    assert isinstance(m, folium.Map)
