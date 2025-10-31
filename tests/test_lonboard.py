"""Test folium plotting functionality."""

import geopandas as gpd
import lonboard
import pytest

from bivario import viz_bivariate_data
from bivario.folium import SCHEME_TYPE
from bivario.lonboard import LonboardMapWithLegend


@pytest.fixture  # type: ignore
def dummy_data() -> gpd.GeoDataFrame:
    """Example geodataframe."""
    return gpd.GeoDataFrame(
        dict(a=[1, 2], b=[10, 100]), geometry=gpd.GeoSeries.from_xy([0, 1], [1, 1], crs=4326)
    )


def test_viz_bivariate_data(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that viz_bivariate_data can be run without error."""
    m = viz_bivariate_data(dummy_data, column_a="a", column_b="b")

    assert isinstance(m, LonboardMapWithLegend)


def test_dark_mode_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    viz_bivariate_data(dummy_data, column_a="a", column_b="b", dark_mode=True)


def test_column_values_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    viz_bivariate_data(dummy_data, column_a=[100, 200], column_b=[41, 53])


def test_alpha_mode_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    viz_bivariate_data(dummy_data, column_a="a", column_b="b", alpha=False)


def test_different_alpha_quantile_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    viz_bivariate_data(dummy_data, column_a="a", column_b="b", alpha_norm_quantile=0.5)


def test_disable_legend(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that explore_bivariate_data can be run without error."""
    m = viz_bivariate_data(dummy_data, column_a="a", column_b="b", legend=False)

    assert isinstance(m, lonboard.Map)


@pytest.mark.parametrize(
    "scheme",
    [
        None,
        True,
        False,
        "Quantiles",
        (True, False),
        (True, None),
        ("NaturalBreaks", "Quantiles"),
    ],
)  # type: ignore
@pytest.mark.parametrize("k", [3, (3, 5)])  # type: ignore
def test_different_schemes(
    nyc_data: gpd.GeoDataFrame,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE],
    k: int | tuple[int, int],
) -> None:
    """Test that dark_mode can be set."""
    viz_bivariate_data(
        nyc_data, column_a="morning_starts", column_b="morning_ends", scheme=scheme, k=k
    )
