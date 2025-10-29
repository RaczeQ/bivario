"""Test folium plotting functionality."""

from typing import Literal

import folium
import geopandas as gpd
import pytest

from bivario import explore_bivariate_data
from bivario.folium import SCHEME_TYPE


@pytest.fixture  # type: ignore
def dummy_data() -> gpd.GeoDataFrame:
    """Example geodataframe."""
    return gpd.GeoDataFrame(
        dict(a=[1, 2], b=[10, 100]), geometry=gpd.GeoSeries.from_xy([0, 1], [1, 1], crs=4326)
    )


def test_explore_bivariate_data(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that explore_bivariate_data can be run without error."""
    m = explore_bivariate_data(dummy_data, column_a="a", column_b="b")

    assert isinstance(m, folium.Map)


def test_dark_mode_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(dummy_data, column_a="a", column_b="b", dark_mode=True)


def test_column_values_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(dummy_data, column_a=[100, 200], column_b=[41, 53])


def test_alpha_mode_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(dummy_data, column_a="a", column_b="b", alpha=False)


def test_different_alpha_quantile_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(dummy_data, column_a="a", column_b="b", alpha_norm_quantile=0.5)


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
    dummy_data: gpd.GeoDataFrame,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE],
    k: int | tuple[int, int],
) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(
        dummy_data, column_a="a", column_b="b", scheme=scheme, k=k, legend_size_px=32
    )


@pytest.mark.parametrize("legend_pos", ["bl", "br", "tl", "tr", None])  # type: ignore
@pytest.mark.parametrize("legend_background", [True, False])  # type: ignore
@pytest.mark.parametrize("legend_border", [True, False])  # type: ignore
def test_different_legend_positions(
    dummy_data: gpd.GeoDataFrame,
    legend_pos: Literal["bl", "br", "tl", "tr"] | None,
    legend_background: bool,
    legend_border: bool,
) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(
        dummy_data,
        column_a="a",
        column_b="b",
        legend_pos=legend_pos,
        legend_background=legend_background,
        legend_border=legend_border,
    )
