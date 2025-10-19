import base64
import io
import warnings
from typing import TYPE_CHECKING, Any, Literal, cast

import folium
import geopandas as gpd
import numpy as np
from branca.element import MacroElement
from folium.template import Template
from mapclassify import classify
from mapclassify.classifiers import _format_intervals
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import rgb2hex
from matplotlib.figure import Figure
from xyzservices import TileProvider

from bivario._legend import DPI, plot_bivariate_legend
from bivario.cmap import (
    ALL_BIVARIATE_MODES_PARAMS,
    BIVARIATE_CMAP_MODES,
    bivariate_from_params,
    get_default_bivariate_params,
)

if TYPE_CHECKING:
    from mapclassify.classifiers import MapClassifier

DARK_MODE_TILES_KEYWORDS = ("dark",)


class FloatBivariateMatplotlibLegend(MacroElement):  # type: ignore[misc]
    """Adds a floating bivariate legend in HTML canvas on top of the map."""

    _template = Template(
        """
            {% macro header(this,kwargs) %}
                <style>
                    #{{this.get_name()}} {
                        position: absolute;
                        pointer-events: none;
                        {%- for property, value in this.css.items() %}
                          {{ property }}: {{ value }};
                        {%- endfor %}
                        }
                </style>
            {% endmacro %}

            {% macro html(this,kwargs) %}
            <img id="{{this.get_name()}}" alt="float_image"
                 src="{{ this.image }}"
                 style="z-index: 999999">
            </img>
            {% endmacro %}
            """
    )

    def __init__(
        self,
        fig: Figure,
        ax: Axes,
        legend_size_px: int,
        legend_loc: Literal["bl", "br", "tl", "tr"] | None = None,
        legend_offset_px: float | tuple[float, float] | None = None,
        legend_background: bool = True,
        legend_border: bool = True,
        padding_top_right_corner: bool = False,
        **kwargs: Any,
    ):
        super().__init__()
        self._name = "FloatImage"
        legend_loc = legend_loc or "bl"

        # if legend_offset_px is None:
        #     match

        # if isinstance(legend_offset_px, (int, float)):
        #     legend_position_x = legend_position_y = legend_offset_px
        # else:
        #     legend_position_x, legend_position_y = legend_offset_px

        self.css = kwargs

        if legend_background:
            self.css["background"] = "rgba(255, 255, 255, 0.8)"
            self.css["padding"] = "2px" if padding_top_right_corner else "0 0 2px 2px"

            if legend_border:
                self.css["border"] = "2px solid rgba(0, 0, 0, 0.2)"
                self.css["border-radius"] = "4px"
                self.css["background-clip"] = "padding-box"

        self.resize_fig(fig=fig, ax=ax, legend_size_px=legend_size_px)

        # fig.canvas.draw()
        # renderer = fig.canvas.get_renderer()

        # # Get bounding boxes (in display / pixel coordinates)
        # bbox_ax = ax.get_window_extent(renderer)  # The axes area (data + ticks + labels)
        # bbox_data = ax.get_position()  # Normalized position in figure

        # # Compute inner data area size (in pixels)
        # data_width_px = bbox_ax.width
        # data_height_px = bbox_ax.height

        # print(f"Initial data area size: {data_width_px:.1f}×{data_height_px:.1f}px")

        # # Calculate scale factor so data area = target_data_px
        # scale = legend_size_px / min(data_width_px, data_height_px)

        # # Compute new figure size (inches)
        # w_in, h_in = self.fig.get_size_inches()
        # new_w_in = w_in * scale
        # new_h_in = h_in * scale

        # fig.set_size_inches(new_w_in, new_h_in)

        # # Redraw with new size
        # fig.canvas.draw()

        # renderer = fig.canvas.get_renderer()

        # # Get bounding boxes (in display / pixel coordinates)
        # bbox_ax = ax.get_window_extent(renderer)  # The axes area (data + ticks + labels)
        # bbox_data = ax.get_position()
        # print(bbox_data)  # Normalized position in figure
        # print(bbox_ax)
        # x0, y0, w, h = bbox_ax.bounds
        # print(x0, y0, w, h)  # Normalized position in figure

        # # Compute inner data area size (in pixels)
        # data_width_px = bbox_ax.width
        # data_height_px = bbox_ax.height

        # print(f"Changed data area size: {data_width_px:.1f}×{data_height_px:.1f}px")

        self.image = "data:image/svg+xml;base64," + self.figure_to_base64_string(fig)

        plt.close()

        self.css.pop("bottom", None)
        self.css.pop("top", None)
        self.css.pop("left", None)
        self.css.pop("right", None)
        self.css.pop("transform", None)

        match legend_loc:
            case "bl":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (5, 40)
                )
                self.css["bottom"] = f"{legend_position_y}px"
                self.css["left"] = f"{legend_position_x}px"
                # translateX = legend_position_x - x0
                # translateY = y0 - legend_position_y
            case "br":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (5, 19)
                )
                self.css["bottom"] = f"{legend_position_y}px"
                self.css["right"] = f"{legend_position_x}px"
                # translateX = legend_position_x + legend_size_px + x0
                # translateY = y0 - legend_position_y
            case "tl":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (10, 79)
                )
                self.css["top"] = f"{legend_position_y}px"
                self.css["left"] = f"{legend_position_x}px"
                # translateX = legend_position_x - x0
                # translateY = y0 + legend_size_px - legend_position_y
            case "tr":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (10, 10)
                )
                self.css["top"] = f"{legend_position_y}px"
                self.css["right"] = f"{legend_position_x}px"
                # translateX = legend_position_x + legend_size_px + x0
                # translateY = y0 + legend_size_px - legend_position_y

        print(self.css)

        # self.transform = f"translate({translateX}px, {translateY}px)"

        # from folium.plugins import FloatImage

        # FloatImage(
        #     data_url,
        #     bottom=0,
        #     left=0,
        #     width=f"{new_fig_size_px}px",
        #     transform=f"translate({translateX}px, {translateY}px)",
        #     pointer_events="none",
        # ).add_to(m)

    # legend_position_x = 50
    # legend_position_y = 80

    # new_fig_size_px = new_w_in * DPI
    # translateX = legend_position_x - x0
    # translateY = -(new_fig_size_px - y0 - 200)
    # translateY = +y0 - legend_position_y
    # print(translateX, translateY)

    # FloatImage(
    #     data_url,
    #     bottom=0,
    #     left=0,
    #     width=f"{new_fig_size_px}px",
    #     transform=f"translate({translateX}px, {translateY}px)",
    #     pointer_events="none",
    # ).add_to(m)

    def resize_fig(
        self, fig: Figure, ax: Axes, legend_size_px: int, tolerance_px: float = 0.1
    ) -> None:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        # Get bounding boxes (in display / pixel coordinates)
        bbox_ax = ax.get_window_extent(renderer)  # The axes area (data + ticks + labels)

        # Compute inner data area size (in pixels)
        data_width_px = bbox_ax.width
        data_height_px = bbox_ax.height

        while (
            abs(legend_size_px - data_width_px) > tolerance_px
            or abs(legend_size_px - data_height_px) > tolerance_px
        ):
            # Calculate scale factor so data area = target_data_px
            scale = legend_size_px / min(data_width_px, data_height_px)

            # Compute new figure size (inches)
            w_in, h_in = fig.get_size_inches()
            new_w_in = w_in * scale
            new_h_in = h_in * scale

            fig.set_size_inches(new_w_in, new_h_in)

            # Redraw with new size
            fig.canvas.draw()

            renderer = fig.canvas.get_renderer()

            # Get bounding boxes (in display / pixel coordinates)
            bbox_ax = ax.get_window_extent(renderer)  # The axes area (data + ticks + labels)

            data_width_px = bbox_ax.width
            data_height_px = bbox_ax.height

        print(f"Changed data area size: {data_width_px:.1f}×{data_height_px:.1f}px")

    def figure_to_base64_string(self, fig: Figure) -> str:
        buffered = io.BytesIO()
        fig.savefig(
            buffered, format="svg", transparent=True, dpi=DPI, bbox_inches="tight", pad_inches=0
        )
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def parse_offset(self, legend_offset_px: float | tuple[float, float]) -> tuple[float, float]:
        if isinstance(legend_offset_px, (int, float)):
            legend_position_x = legend_position_y = legend_offset_px
        else:
            legend_position_x, legend_position_y = legend_offset_px
        return (legend_position_x, legend_position_y)


def explore_bivariate_data(
    gdf: gpd.GeoDataFrame,
    column_a: str,
    column_b: str,  # enable list of values
    column_a_label: str | None = None,
    column_b_label: str | None = None,
    scheme: str | None | bool = True,
    k: int = 5,
    tiles: str | folium.TileLayer | TileProvider | None = None,
    cmap_mode: BIVARIATE_CMAP_MODES = "name",
    cmap_params: ALL_BIVARIATE_MODES_PARAMS | None = None,
    cmap_kwargs: dict[str, Any] | None = None,
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
) -> folium.Map:
    # schema
    # k
    # alpha - yes / no - allow iterable as list of floats between 0 and 1
    # alpha_norm_quantile = 0.9 - make sure between 0 and 1

    # check if columns exist, and allow passing values that have the same length

    set_alpha = alpha  # now its bool, but can be a list of values, then check if not empty

    if cmap_params is None:
        cmap_params = get_default_bivariate_params(cmap_mode)

    values_a = gdf[column_a]
    values_b = gdf[column_b]

    # If tiles are not defined - set based on dark mode
    if tiles is None:
        if dark_mode is None:
            dark_mode = False

        tiles = "CartoDB DarkMatter" if dark_mode else "CartoDB Positron"
    # If tiles are defined, set dark mode based on tiles if not defined
    else:
        dark_mode = False
        tiles_name = ""
        if isinstance(tiles, str):
            tiles_name = tiles.lower()
        elif isinstance(tiles, TileProvider):
            tiles_name = str(tiles.name).lower()

        for keyword in DARK_MODE_TILES_KEYWORDS:
            if keyword in tiles_name:
                dark_mode = True
                break

    cmap_kwargs = cmap_kwargs or {}
    if "dark_mode" not in cmap_kwargs:
        cmap_kwargs["dark_mode"] = dark_mode

    tick_labels_a = None
    tick_labels_b = None

    if isinstance(scheme, bool):
        scheme = "NaturalBreaks" if scheme else None

    if scheme is not None:
        binning_a = cast("MapClassifier", classify(values_a, scheme=scheme, k=k))
        binning_b = cast("MapClassifier", classify(values_b, scheme=scheme, k=k))

        values_a = binning_a.yb
        values_b = binning_b.yb

        tick_labels_a = [_l.replace(".0", "") for _l in _format_intervals(binning_a, "{:.1f}")[0]]
        tick_labels_b = [_l.replace(".0", "") for _l in _format_intervals(binning_b, "{:.1f}")[0]]

        print(tick_labels_a)
        print(tick_labels_b)

        # tick_labels_a = [0, binning_a.bins]

    values_cmap = bivariate_from_params(
        values_a=values_a,
        values_b=values_b,
        mode=cmap_mode,
        params=cmap_params,
        **cmap_kwargs,
    )

    hex_values = [rgb2hex(values_cmap[i, :]) for i in range(values_cmap.shape[0])]

    if set_alpha:
        alpha_values = np.sqrt(
            np.minimum(
                1,
                np.maximum(
                    gdf[column_a] / gdf[column_a].quantile(alpha_norm_quantile),
                    gdf[column_b] / gdf[column_b].quantile(alpha_norm_quantile),
                ),
            )
        ).tolist()
        if "style_kwds" not in kwargs:
            kwargs["style_kwds"] = {}

        kwargs["style_kwds"]["style_function"] = lambda x: dict(
            opacity=0, fillOpacity=alpha_values[int(x["id"])]
        )

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
        legend_kwargs = legend_kwargs or {}
        # print(legend_kwargs)

        fig, ax = plt.subplots(dpi=DPI, layout="compressed")
        plot_bivariate_legend(
            ax=ax,
            values_a=gdf[column_a],
            values_b=gdf[column_b],
            cmap_mode=cmap_mode,
            cmap_params=cmap_params,
            label_a=column_a_label,
            label_b=column_b_label,
            tick_labels_a=tick_labels_a,
            tick_labels_b=tick_labels_b,
            font_colour="#333" if legend_background else None,
            grid_size=legend_size_px if scheme is None else k,
            **cmap_kwargs,
            **legend_kwargs,
        )

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
