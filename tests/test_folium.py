"""Test folium plotting functionality."""

from typing import Literal

import folium
import geopandas as gpd
import pytest

from bivario import explore_bivariate_data
from bivario._scheme import SCHEME_TYPE
from bivario.folium._basemap import MapLibreLayer
from bivario.folium._legend import FloatBivariateMatplotlibLegend


def test_explore_bivariate_data(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that explore_bivariate_data can be run without error."""
    m = explore_bivariate_data(dummy_data, column_a="a", column_b="b")

    assert isinstance(m, folium.Map)


def test_dark_mode_plotting(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that dark_mode can be set."""
    explore_bivariate_data(dummy_data, column_a="a", column_b="b", dark_mode=True)


@pytest.mark.parametrize(
    ("dark_mode", "style"), [(None, "positron"), (False, "positron"), (True, "dark")]
)  # type: ignore
def test_default_tiles(dummy_data: gpd.GeoDataFrame, dark_mode: bool | None, style: str) -> None:
    """Test that the default basemap is a vector style of OpenFreeMap."""
    html = (
        explore_bivariate_data(dummy_data, column_a="a", column_b="b", dark_mode=dark_mode)
        .get_root()
        .render()
    )

    assert f"https://tiles.openfreemap.org/styles/{style}" in html
    assert "leaflet-maplibre-gl.js" in html
    assert "L.tileLayer" not in html


def test_custom_tiles(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that given tiles replace the default basemap."""
    html = (
        explore_bivariate_data(dummy_data, column_a="a", column_b="b", tiles="OpenStreetMap")
        .get_root()
        .render()
    )

    assert "tile.openstreetmap.org" in html
    assert "openfreemap" not in html


def test_zoom_limits(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that given zoom limits apply to the default basemap."""
    html = (
        explore_bivariate_data(dummy_data, column_a="a", column_b="b", min_zoom=5, max_zoom=12)
        .get_root()
        .render()
    )

    assert "minZoom: 5, maxZoom: 12" in html


def test_basemap_attaches_itself() -> None:
    """Test that the basemap adds itself to the map, as Folium < 0.15 does not do it."""
    m = folium.Map(tiles=None)
    layer = MapLibreLayer("style.json").add_to(m)

    script = layer._template.module.script(layer, {})

    assert f"{layer.get_name()}.addTo({m.get_name()});" in script


def test_constant_values(dummy_data: gpd.GeoDataFrame) -> None:
    """Test that columns of constant values can be plotted."""
    explore_bivariate_data(dummy_data, column_a=[5, 5], column_b=[7, 7])
    explore_bivariate_data(dummy_data, column_a=[5, 5], column_b="b", scheme=False)


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
