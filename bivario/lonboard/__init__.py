"""Bivariate lonboard maps module."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, cast, overload

import narwhals as nw
import numpy as np

from bivario._alpha import prepare_alpha_values
from bivario._constants import DARK_MODE_TILES_KEYWORDS
from bivario._scheme import SCHEME_TYPE, apply_mapclassify
from bivario.cmap import BivariateColourmap, _validate_values, get_bivariate_cmap
from bivario.legend import plot_bivariate_legend, resize_fig

if TYPE_CHECKING:
    from collections.abc import Callable

    from lonboard._map import Map
    from lonboard.types.layer import (
        PathLayerKwargs,
        PolygonLayerKwargs,
        ScatterplotLayerKwargs,
    )
    from lonboard.types.map import MapKwargs
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from narwhals.typing import IntoFrame

    from bivario.typing import ValueInput


@dataclass
class LonboardMapWithLegend:
    """Lonboard Map object with bivariate legend as Matplotlib Axes."""

    m: "Map"
    legend: "Callable[..., Axes]"

    def _repr_mimebundle_(self, **kwargs: dict) -> tuple[dict, dict] | None:  # type: ignore[type-arg]
        # Delegate rendering to the map object
        if hasattr(self.m, "_repr_mimebundle_"):
            return self.m._repr_mimebundle_(**kwargs)  # type: ignore[no-any-return]

        return None


@overload
def viz_bivariate_data(
    data: "Any | list[Any] | tuple[Any, ...]",
    column_a: "str | ValueInput",
    column_b: "str | ValueInput",
    column_a_label: str | None = None,
    column_b_label: str | None = None,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE] = True,
    k: int | tuple[int, int] = 5,
    tiles: str | None = None,
    cmap: BivariateColourmap | str | None = None,
    dark_mode: bool | None = None,
    alpha: bool = True,
    alpha_norm_quantile: float = 0.9,
    legend: Literal[True] = True,
    legend_size_px: int = 400,
    legend_max_grid_size: int | None = 100,
    legend_tick_fontsize_px: int = 16,
    legend_kwargs: dict[str, Any] | None = None,
    scatterplot_kwargs: "ScatterplotLayerKwargs | None" = None,
    path_kwargs: "PathLayerKwargs | None" = None,
    polygon_kwargs: "PolygonLayerKwargs | None" = None,
    map_kwargs: "MapKwargs | None" = None,
) -> "LonboardMapWithLegend": ...


@overload
def viz_bivariate_data(
    data: "Any | list[Any] | tuple[Any, ...]",
    column_a: "str | ValueInput",
    column_b: "str | ValueInput",
    column_a_label: str | None = None,
    column_b_label: str | None = None,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE] = True,
    k: int | tuple[int, int] = 5,
    tiles: str | None = None,
    cmap: BivariateColourmap | str | None = None,
    dark_mode: bool | None = None,
    alpha: bool = True,
    alpha_norm_quantile: float = 0.9,
    legend: Literal[False] = False,
    legend_size_px: int = 400,
    legend_max_grid_size: int | None = 100,
    legend_tick_fontsize_px: int = 16,
    legend_kwargs: dict[str, Any] | None = None,
    scatterplot_kwargs: "ScatterplotLayerKwargs | None" = None,
    path_kwargs: "PathLayerKwargs | None" = None,
    polygon_kwargs: "PolygonLayerKwargs | None" = None,
    map_kwargs: "MapKwargs | None" = None,
) -> "Map": ...


def viz_bivariate_data(
    data: "Any | list[Any] | tuple[Any, ...]",
    column_a: "str | ValueInput",
    column_b: "str | ValueInput",
    column_a_label: str | None = None,
    column_b_label: str | None = None,
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE] = True,
    k: int | tuple[int, int] = 5,
    tiles: str | None = None,
    cmap: BivariateColourmap | str | None = None,
    dark_mode: bool | None = None,
    alpha: bool = True,
    alpha_norm_quantile: float = 0.9,
    legend: bool = True,
    legend_size_px: int = 400,
    legend_max_grid_size: int | None = 100,
    legend_tick_fontsize_px: int = 16,
    legend_kwargs: dict[str, Any] | None = None,
    scatterplot_kwargs: "ScatterplotLayerKwargs | None" = None,
    path_kwargs: "PathLayerKwargs | None" = None,
    polygon_kwargs: "PolygonLayerKwargs | None" = None,
    map_kwargs: "MapKwargs | None" = None,
) -> "Map | LonboardMapWithLegend":
    """
    Visualize geospatial data with a bivariate colormap on a lonboard map.

    Args:
        data (Any | list[Any] | tuple[Any, ...]): Geospatial data to plot. Any compatible with
            lonboard viz function.
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
        tiles (str | None, optional): Tile layer for the map. If None, will set based
            on dark mode - "CartoDB DarkMatter" for the dark mode, and "CartoDB Positron"
            for the light mode. Defaults to None.
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
        legend (bool, optional): Whether to return a lonboard map with a legend plotting function.
            If True, will return LonboardMapWithLegend object with lonboard map and legend function.
            If False, will return lonboard.Map. Defaults to True.
        legend_size_px (int, optional): Size of the legend in pixels. Defaults to 400.
        legend_max_grid_size (int | None, optional): Max size of the legend grid used for plotting
            the legend. Used with scheme=False. Defaults to 100.
        legend_tick_fontsize_px (int, optional): Size of the ticks and labels for the legend
            in pixels. Defaults to 16.
        legend_kwargs (dict[str, Any] | None, optional): Additional keyword arguments for the
            legend plotting function. Defaults to None.
        scatterplot_kwargs: a `dict` of parameters to pass down to all generated
            lonboard.ScatterplotLayers.
        path_kwargs: a `dict` of parameters to pass down to all generated
            lonboard.PathLayers.
        polygon_kwargs: a `dict` of parameters to pass down to all generated
            lonboard.PolygonLayers.
        map_kwargs: a `dict` of parameters to pass down to the generated
            lonboard.Map.

    Returns:
        lonboard.Map | LonboardMapWithLegend: Lonboard map with the bivariate colormap applied or
            object with lonboard map and legend plotting function.

    Examples:
        Plot NYC bike trips with morning starts and ends:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import viz_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> x = viz_bivariate_data(
        ...     gdf,
        ...     column_a="morning_starts",
        ...     column_b="morning_ends",
        ... )
        >>> x
        LonboardMapWithLegend(...)

        Display a legend in another cell:
        >>> x.legend()
        <Axes: xlabel='morning_ends', ylabel='morning_starts'>

        Get lonboard.Map object from the result:
        >>> x.m
        Map(...)

        Plot in dark mode with different colormap and different binning:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import viz_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> viz_bivariate_data(
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
        LonboardMapWithLegend(...)

        Plot without binning (numerical values) and add tooltip to map:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import viz_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> viz_bivariate_data(
        ...     gdf,
        ...     column_a="morning_starts",
        ...     column_b="afternoon_starts",
        ...     scheme=False,
        ...     map_kwargs={"show_tooltip": True},
        ... )
        LonboardMapWithLegend(...)

        Plot without legend and get lonboard Map directly:
        >>> from bivario.example_data import nyc_bike_trips
        >>> from bivario import viz_bivariate_data
        >>> gdf = nyc_bike_trips()
        >>> viz_bivariate_data(
        ...     gdf,
        ...     column_a="morning_starts",
        ...     column_b="morning_ends",
        ...     legend=False,
        ... )
        Map(...)
    """
    try:
        from lonboard import viz
        from lonboard.basemap import CartoBasemap
    except (ImportError, ModuleNotFoundError) as ex:
        raise ImportError(
            "The 'lonboard>=0.10' package "
            "is required for plotting lonboard map. You can install it using "
            "'conda install -c conda-forge \"lonboard>=0.10\"' "
            "or 'pip install \"lonboard>=0.10\"'."
        ) from ex

    narwhals_df = None

    if isinstance(column_a, str) or isinstance(column_b, str):
        try:
            cols_to_select = []
            if isinstance(column_a, str):
                cols_to_select.append(column_a)
            if isinstance(column_b, str):
                cols_to_select.append(column_b)

            narwhals_df = nw.from_native(cast("IntoFrame", data)).select(*cols_to_select)

            if isinstance(narwhals_df, nw.LazyFrame):
                narwhals_df = narwhals_df.collect()

            original_values_a = narwhals_df[column_a] if isinstance(column_a, str) else column_a
            original_values_b = narwhals_df[column_b] if isinstance(column_b, str) else column_b
        except TypeError as ex:
            raise TypeError(
                "Cannot parse provided input as a source for loading str column."
            ) from ex
    else:
        original_values_a = column_a
        original_values_b = column_b

    values_a, values_b = _validate_values(original_values_a, original_values_b)

    # If tiles are not defined - set based on dark mode
    if tiles is None:
        if dark_mode is None:
            dark_mode = False

        tiles = CartoBasemap.DarkMatter if dark_mode else CartoBasemap.Positron
    # If tiles are defined, set dark mode based on tiles if not defined
    elif dark_mode is None:
        dark_mode = False
        tiles_name = tiles.lower()

        for keyword in DARK_MODE_TILES_KEYWORDS:
            if keyword in tiles_name:
                dark_mode = True
                break

    set_alpha = alpha  # now its bool, but can be a list of values, then check if not empty

    alpha_values = None

    if set_alpha:
        alpha_values = prepare_alpha_values(
            values_a=values_a, values_b=values_b, alpha_norm_quantile=alpha_norm_quantile
        ).reshape(-1, 1)

    scheme_result = apply_mapclassify(values_a=values_a, values_b=values_b, scheme=scheme, k=k)

    cmap = get_bivariate_cmap(cmap)

    values_cmap = cmap(
        values_a=scheme_result.values_a,
        values_b=scheme_result.values_b,
        normalize=True,
        dark_mode=dark_mode,
    )

    if alpha_values is not None:
        values_cmap = np.concatenate([values_cmap, alpha_values], axis=1)

    values_cmap = (values_cmap * 255).astype(np.uint8)

    map_kwargs = map_kwargs or {}
    polygon_kwargs = polygon_kwargs or {}
    scatterplot_kwargs = scatterplot_kwargs or {}
    path_kwargs = path_kwargs or {}

    map_kwargs["basemap_style"] = tiles

    # Polygon layer
    polygon_kwargs["filled"] = True
    polygon_kwargs["get_fill_color"] = values_cmap

    if "stroked" not in polygon_kwargs:
        polygon_kwargs["stroked"] = False
    if "opacity" not in polygon_kwargs:
        polygon_kwargs["opacity"] = 1

    # Scatterplot layer
    scatterplot_kwargs["filled"] = True
    scatterplot_kwargs["get_fill_color"] = values_cmap

    if "stroked" not in scatterplot_kwargs:
        scatterplot_kwargs["stroked"] = False
    if "opacity" not in scatterplot_kwargs:
        scatterplot_kwargs["opacity"] = 1

    # Path layer
    path_kwargs["get_color"] = values_cmap

    if "opacity" not in path_kwargs:
        path_kwargs["opacity"] = 1

    m = viz(
        data=data,
        map_kwargs=map_kwargs,
        polygon_kwargs=polygon_kwargs,
        scatterplot_kwargs=scatterplot_kwargs,
        path_kwargs=path_kwargs,
    )

    if legend:
        legend_kwargs = legend_kwargs or {}

        grid_size: int | tuple[int, int]
        numerical_grid_size = legend_max_grid_size or legend_size_px
        if scheme_result.scheme_a is scheme_result.scheme_b is None:
            grid_size = numerical_grid_size
        else:
            grid_size_y = (
                numerical_grid_size if scheme_result.scheme_a is None else scheme_result.k_a
            )
            grid_size_x = (
                numerical_grid_size if scheme_result.scheme_b is None else scheme_result.k_b
            )
            grid_size = (grid_size_x, grid_size_y)

        def display_legend() -> "Axes":
            ax = plot_bivariate_legend(
                values_a=original_values_a,
                values_b=original_values_b,
                cmap=cmap,
                label_a=column_a_label,
                label_b=column_b_label,
                tick_labels_a=scheme_result.tick_labels_a,
                tick_labels_b=scheme_result.tick_labels_b,
                font_colour="black",
                grid_size=grid_size,
                dark_mode=dark_mode,
                tick_fontsize_px=legend_tick_fontsize_px,
                **legend_kwargs,
            )
            fig = cast("Figure", ax.figure)
            resize_fig(fig=fig, ax=ax, legend_size_px=legend_size_px)
            # plt.show()

            return ax

        return LonboardMapWithLegend(m=m, legend=display_legend)

    return m
