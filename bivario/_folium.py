import base64
import warnings
from typing import Any, Literal, Optional, Union

import folium
import geopandas as gpd
import numpy as np
import numpy.typing as npt
from matplotlib import pyplot as plt
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

DARK_MODE_TILES_KEYWORDS = ("dark",)

from branca.element import MacroElement
from folium.template import Template


# class FloatBivariateMatplotlibLegend(MacroElement):
#     """Adds a floating bivariate legend in HTML canvas on top of the map."""

#     _template = Template(
#         """
#             {% macro header(this,kwargs) %}
#                 <style>
#                     #{{this.get_name()}} {
#                         position: absolute;
#                         bottom: {{this.bottom}}%;
#                         left: {{this.left}}%;
#                         {%- for property, value in this.css.items() %}
#                           {{ property }}: {{ value }};
#                         {%- endfor %}
#                         }
#                 </style>
#             {% endmacro %}

#             {% macro html(this,kwargs) %}
#             <img id="{{this.get_name()}}" alt="float_image"
#                  src="{{ this.image }}"
#                  style="z-index: 999999">
#             </img>
#             {% endmacro %}
#             """
#     )

#     def __init__(self, image, bottom=75, left=75, **kwargs):
#         super().__init__()
#         self._name = "FloatImage"
#         self.image = image
#         self.bottom = bottom
#         self.left = left
#         self.css = kwargs

#     # legend_position_x = 50
#     # legend_position_y = 80

#     # new_fig_size_px = new_w_in * DPI
#     # translateX = legend_position_x - x0
#     # translateY = -(new_fig_size_px - y0 - 200)
#     # translateY = +y0 - legend_position_y
#     # print(translateX, translateY)

#     # FloatImage(
#     #     data_url,
#     #     bottom=0,
#     #     left=0,
#     #     width=f"{new_fig_size_px}px",
#     #     transform=f"translate({translateX}px, {translateY}px)",
#     #     pointer_events="none",
#     # ).add_to(m)

#     def figure_to_base64_string(self, plt_fig: Figure):
#         import io

#         buffered = io.BytesIO()
#         # img.save(buffered, format="PNG")
#         # plt_fig.tight_layout()
#         plt_fig.savefig(buffered, transparent=True, dpi=DPI)
#         # plt_fig.savefig(buffered, dpi=DPI)
#         return base64.b64encode(buffered.getvalue()).decode("utf-8")


def explore_bivariate_data(
    gdf: gpd.GeoDataFrame,
    column_a: str,
    column_b: str,  # enable list of values
    tiles: str | folium.TileLayer | TileProvider | None = None,
    cmap_mode: BIVARIATE_CMAP_MODES = "name",
    cmap_params: ALL_BIVARIATE_MODES_PARAMS | None = None,
    cmap_kwargs: dict[str, Any] | None = None,
    dark_mode: bool | None = None,
    alpha: bool = True,
    alpha_norm_quantile: float = 0.9,
    legend: bool = True,
    legend_size_px=200,
    legend_loc: Literal["bl", "br", "tl", "tr"] = "bl",
    legend_offset_px: float | tuple[float, float] = (50, 80),
    **kwargs,
) -> folium.Map:
    # tiles
    # schema
    # k
    # alpha - yes / no - allow iterable as list of floats between 0 and 1
    # alpha_norm_quantile = 0.9 - make sure between 0 and 1
    # dark_mode: bool - default None, take from tiles
    # legend_size - how many pixels - default - the same as number of pixels
    # legend_loc - bottom_left (default), bottom_right, top_left, top_right
    # legend_offset_px - how far from corner, in pixels (one digit or two - xy)
    # legend_size_px
    # legend - default True, allow False
    # disallow folium legend - remove from kwargs if exists

    # check if columns exist, and allow passing values that have the same length

    set_alpha = alpha

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

    values_cmap = bivariate_from_params(
        values_a=values_a,
        values_b=values_b,
        mode=cmap_mode,
        params=cmap_params,
        **cmap_kwargs,
    )

    hex_values = [rgb2hex(values_cmap[i, :]) for i in range(values_cmap.shape[0])]
    # color_dict = dict(zip(gdf.index, hex_values))

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

    # IMAGE_SIZE_PX = 250

    # IMG_SIZE_IN = IMAGE_SIZE_PX / DPI

    m = gdf.explore(
        color=hex_values,
        legend=False,
        tiles=tiles,
        embed=True,
        **kwargs,
    )

    if legend:
        img_size_in = legend_size_px / DPI
        fig, ax = plt.subplots(figsize=(img_size_in, img_size_in), dpi=DPI, constrained_layout=True)
        legend = plot_bivariate_legend(
            ax=ax,
            values_a=gdf[column_a],
            values_b=gdf[column_b],
            dark_mode=dark_mode,
        )

    return m
