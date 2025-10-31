"""Test folium plotting functionality."""

from typing import Literal

import folium
import geopandas as gpd
import pytest

from bivario import explore_bivariate_data
from bivario.folium import SCHEME_TYPE
from bivario.folium._legend import FloatBivariateMatplotlibLegend


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
    nyc_data: gpd.GeoDataFrame,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE],
    k: int | tuple[int, int],
) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(
        nyc_data,
        column_a="morning_starts",
        column_b="morning_ends",
        scheme=scheme,
        k=k,
        legend_size_px=32,
    )


@pytest.mark.parametrize("legend_loc", ["bl", "br", "tl", "tr", None])  # type: ignore
@pytest.mark.parametrize("legend_background", [True, False])  # type: ignore
@pytest.mark.parametrize("legend_border", [True, False])  # type: ignore
def test_different_legend_positions(
    dummy_data: gpd.GeoDataFrame,
    legend_loc: Literal["bl", "br", "tl", "tr"] | None,
    legend_background: bool,
    legend_border: bool,
) -> None:
    """Test that dark_mode can be set."""
    m = explore_bivariate_data(
        dummy_data,
        column_a="a",
        column_b="b",
        legend_loc=legend_loc,
        legend_background=legend_background,
        legend_border=legend_border,
    )

    legend_object = [
        v for v in m.__dict__["_children"].values() if isinstance(v, FloatBivariateMatplotlibLegend)
    ][0]

    expected_legend_loc = legend_loc or "bl"

    if "b" in expected_legend_loc:
        assert "bottom" in legend_object.css
    if "t" in expected_legend_loc:
        assert "top" in legend_object.css
    if "l" in expected_legend_loc:
        assert "left" in legend_object.css
    if "r" in expected_legend_loc:
        assert "right" in legend_object.css

    if legend_background:
        assert "background" in legend_object.css
        assert "padding" in legend_object.css

        if legend_border:
            assert "border" in legend_object.css
            assert "border-radius" in legend_object.css
            assert "background-clip" in legend_object.css
