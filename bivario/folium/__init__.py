"""Bivariate folium maps module."""

import warnings
from typing import TYPE_CHECKING, Any, Literal, cast

import numpy as np
from mapclassify import classify
from mapclassify.classifiers import _format_intervals
from matplotlib.colors import rgb2hex

from bivario.cmap import BivariateColourmap, _validate_values, get_bivariate_cmap
from bivario.legend import plot_bivariate_legend

if TYPE_CHECKING:
    import folium
    import geopandas as gpd
    import xyzservices
    from mapclassify.classifiers import MapClassifier
    from matplotlib.figure import Figure

    from bivario.typing import ValueInput

DARK_MODE_TILES_KEYWORDS = ("dark",)


SCHEME_TYPE = str | None | bool


def explore_bivariate_data(
    gdf: "gpd.GeoDataFrame",
    column_a: "str | ValueInput",
    column_b: "str | ValueInput",
    column_a_label: str | None = None,
    column_b_label: str | None = None,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE] = True,
    k: int | tuple[int, int] = 5,
    tiles: "str | folium.TileLayer | xyzservices.TileProvider | None" = None,
    cmap: BivariateColourmap | str | None = None,
    dark_mode: bool | None = None,
    alpha: bool = True,
    alpha_norm_quantile: float = 0.9,
    legend: bool = True,
    legend_size_px: int = 200,
    legend_loc: Literal["bl", "br", "tl", "tr"] | None = None,
    legend_offset_px: float | tuple[float, float] | None = None,
    legend_background: bool = True,
    legend_border: bool = True,
    legend_kwargs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> "folium.Map":
    """
    Explore geospatial data with a bivariate colormap on a folium map.

    Args:
        gdf (gpd.GeoDataFrame): Geospatial data to plot.
        column_a (str | ValueInput): Column name for the first variable or list/array of values.
        column_b (str | ValueInput): Column name for the second variable or list/array of values.
        column_a_label (str | None, optional): Label for column a. If None, will use column name.
            Defaults to None.
        column_b_label (str | None, optional): Label for column b. If None, will use column name.
            Defaults to None.
        scheme (str | None | bool | tuple, optional): Mapclassify binning scheme for the data.
            If True, uses "NaturalBreaks". If False, no binning is applied.
            If str, uses the specified scheme. If None, no binning is applied. Can also define
            two different values for columns a and b. Defaults to True.
        k (int | tuple[int, int], optional): Number of classes for binning. Can also define two
            different values for columns a and b. Defaults to 5.
        tiles (str | folium.TileLayer | xyzservices.TileProvider | None, optional): Tile layer
            for the map. If None, will set based on dark mode - "CartoDB DarkMatter" for the
            dark mode, and "CartoDB Positron" for the light mode. Defaults to None.
        cmap (BivariateColourmap | str | None, optional): Bivariate colourmap to use.
            If None, will load a default one. Defaults to None.
        dark_mode (bool | None, optional): Whether to use dark mode for the map tiles. If None,
            will infer from the tiles if provided, otherwise defaults to False. Defaults to None
        alpha (bool, optional): Whether to apply alpha transparency based on the data values. Will
            set higher values to be more opaque. It is calculated based on the normalized values of
            both columns. Defaults to True.
        alpha_norm_quantile (float, optional): Quantile for normalizing alpha transparency.
            Will be used to calculate the maximum value for alpha scaling. It is recommended to use
            value below 1 to avoid outliers affecting the transparency too much. Defaults to 0.9.
        legend (bool, optional): Whether to add a bivariate legend to the map. Defaults to True.
        legend_size_px (int, optional): Size of the legend in pixels. Defaults to 200.
        legend_loc (Literal["bl", "br", "tl", "tr"] | None, optional): Location of the legend
            on the map. Can be "bl" (bottom-left), "br" (bottom-right), "tl" (top-left),
            or "tr" (top-right). Defaults to "bl".
        legend_offset_px (float | tuple[float, float] | None, optional): Offset of the legend
            from the specified location in pixels. If None, uses default offsets based on location.
            Defaults to None.
        legend_background (bool, optional): Whether to add a background to the legend.
            Defaults to True.
        legend_border (bool, optional): Whether to add a border to the legend. Defaults to True.
        legend_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the
            legend plotting function. Defaults to None.
        **kwargs (Any): Additional keyword arguments for the folium map.

    Returns:
        folium.Map: Folium map with the bivariate colormap applied.

    Examples:
        Plot NYC bike trips with morning starts and ends:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import explore_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> explore_bivariate_data(
        ...     gdf,
        ...     column_a="morning_starts",
        ...     column_b="morning_ends",
        ... )
        <folium.folium.Map object at 0x...>

        Plot in dark mode with different colormap and different binning:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import explore_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> explore_bivariate_data(
        ...     gdf,
        ...     column_a="morning_starts",
        ...     column_b="morning_ends",
        ...     column_a_label="Morning Starts",
        ...     column_b_label="Morning Ends",
        ...     dark_mode=True,
        ...     cmap="bubblegum",
        ...     scheme="Quantiles",
        ...     k=10,
        ... )
        <folium.folium.Map object at 0x...>

        Plot without binning (numerical values) and different legend position:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import explore_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> explore_bivariate_data(
        ...     gdf,
        ...     column_a="morning_starts",
        ...     column_b="afternoon_starts",
        ...     scheme=False,
        ...     legend_loc="tr",
        ...     legend_size_px=300,
        ... )
        <folium.folium.Map object at 0x...>
    """
    # alpha - yes / no - allow iterable as list of floats between 0 and 1

    for column in (column_a, column_b):
        if isinstance(column, str) and column not in gdf.columns:
            raise ValueError(f"Column '{column}' not found in GeoDataFrame.")

    original_values_a = gdf[column_a] if isinstance(column_a, str) else column_a
    original_values_b = gdf[column_b] if isinstance(column_b, str) else column_b

    _values_a, _values_b = _validate_values(
        gdf[column_a] if isinstance(column_a, str) else column_a,
        gdf[column_b] if isinstance(column_b, str) else column_b,
    )

    # If tiles are not defined - set based on dark mode
    if tiles is None:
        if dark_mode is None:
            dark_mode = False

        tiles = "CartoDB DarkMatter" if dark_mode else "CartoDB Positron"
    # If tiles are defined, set dark mode based on tiles if not defined
    elif dark_mode is None:
        dark_mode = False
        tiles_name = ""
        if isinstance(tiles, str):
            tiles_name = tiles.lower()
        elif hasattr(tiles, "name"):
            tiles_name = str(tiles.name).lower()

        for keyword in DARK_MODE_TILES_KEYWORDS:
            if keyword in tiles_name:
                dark_mode = True
                break

    set_alpha = alpha  # now its bool, but can be a list of values, then check if not empty

    if set_alpha:
        if alpha_norm_quantile < 0 or alpha_norm_quantile > 1:
            raise ValueError("alpha_norm_quantile must be between 0 and 1 (inclusive).")

        alpha_values = np.sqrt(
            np.minimum(
                1,
                np.maximum(
                    _values_a / np.quantile(_values_a, alpha_norm_quantile),
                    _values_b / np.quantile(_values_b, alpha_norm_quantile),
                ),
            )
        ).tolist()
        if "style_kwds" not in kwargs:
            kwargs["style_kwds"] = {}

        kwargs["style_kwds"]["style_function"] = lambda x: dict(
            opacity=0, fillOpacity=alpha_values[int(x["id"])]
        )

    tick_labels_a = None
    tick_labels_b = None

    if isinstance(scheme, (tuple, list)):
        scheme_a, scheme_b = scheme
    else:
        scheme_a = scheme_b = scheme

    if isinstance(k, (tuple, list)):
        k_a, k_b = k
    else:
        k_a = k_b = k

    if isinstance(scheme_a, bool):
        scheme_a = "NaturalBreaks" if scheme_a else None
    if isinstance(scheme_b, bool):
        scheme_b = "NaturalBreaks" if scheme_b else None

    if scheme_a is not None:
        binning_a = cast("MapClassifier", classify(_values_a, scheme=scheme_a, k=k_a))
        _values_a = binning_a.yb
        tick_labels_a = [_l.replace(".0", "") for _l in _format_intervals(binning_a, "{:,.1f}")[0]]

    if scheme_b is not None:
        binning_b = cast("MapClassifier", classify(_values_b, scheme=scheme_b, k=k_b))
        _values_b = binning_b.yb
        tick_labels_b = [_l.replace(".0", "") for _l in _format_intervals(binning_b, "{:,.1f}")[0]]

    cmap = get_bivariate_cmap(cmap)

    values_cmap = cmap(values_a=_values_a, values_b=_values_b, normalize=True, dark_mode=dark_mode)

    hex_values = [rgb2hex(tuple(values_cmap[i, :])) for i in range(values_cmap.shape[0])]

    if "legend" in kwargs:
        kwargs.pop("legend")

    if "embed" in kwargs:
        kwargs.pop("embed")
        warnings.warn(
            "Embed folium parameter must be set to true. Ignoring user definition.", stacklevel=0
        )

    m = gdf.explore(
        color=hex_values,
        legend=False,
        tiles=tiles,
        embed=True,
        **kwargs,
    )

    if legend:
        from bivario.folium._legend import FloatBivariateMatplotlibLegend

        legend_kwargs = legend_kwargs or {}

        grid_size: int | tuple[int, int]
        if scheme_a is scheme_b is None:
            grid_size = legend_size_px
        else:
            grid_size_y = legend_size_px if scheme_a is None else k_a
            grid_size_x = legend_size_px if scheme_b is None else k_b
            grid_size = (grid_size_x, grid_size_y)

        ax = plot_bivariate_legend(
            values_a=original_values_a,
            values_b=original_values_b,
            cmap=cmap,
            label_a=column_a_label,
            label_b=column_b_label,
            tick_labels_a=tick_labels_a,
            tick_labels_b=tick_labels_b,
            font_colour="#333" if legend_background else None,
            grid_size=grid_size,
            dark_mode=dark_mode,
            **legend_kwargs,
        )

        fig = cast("Figure", ax.figure)

        FloatBivariateMatplotlibLegend(
            fig=fig,
            ax=ax,
            legend_size_px=legend_size_px,
            legend_loc=legend_loc,
            legend_offset_px=legend_offset_px,
            legend_background=legend_background,
            legend_border=legend_border,
            padding_top_right_corner=scheme is not None,
        ).add_to(m)

    return m
