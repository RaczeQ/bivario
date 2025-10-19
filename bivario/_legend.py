from typing import TYPE_CHECKING, Any

import narwhals as nw
import numpy as np
from matplotlib.axes import Axes
from PIL import Image

from bivario.cmap import (
    ALL_BIVARIATE_MODES_PARAMS,
    BIVARIATE_CMAP_MODES,
    bivariate_from_params,
    get_default_bivariate_params,
)

if TYPE_CHECKING:
    from narwhals.typing import IntoSeries

DPI = 100


def plot_bivariate_legend(
    ax: Axes,
    values_a: "IntoSeries",
    values_b: "IntoSeries",
    cmap_mode: BIVARIATE_CMAP_MODES = "name",
    cmap_params: ALL_BIVARIATE_MODES_PARAMS | None = None,
    cmap_kwargs: dict[str, Any] | None = None,
    grid_size: int | None = None,
    label_a: str | None = None,
    label_b: str | None = None,
    tick_labels_a: list[Any] | None = None,
    tick_labels_b: list[Any] | None = None,
    dark_mode: bool = False,
    font_colour: str | None = None,
    tick_fontsize_px: int = 10,
) -> None:
    if (tick_labels_a is not None and tick_labels_b is None) or (
        tick_labels_a is None and tick_labels_b is not None
    ):
        raise ValueError("Both tick labels for a and b values must be either None, or present.")
    parsed_values_a = nw.from_native(values_a, series_only=True)
    parsed_values_b = nw.from_native(values_b, series_only=True)

    cmap_params = cmap_params or get_default_bivariate_params(cmap_mode)

    cmap_kwargs = cmap_kwargs or {}
    if "dark_mode" not in cmap_kwargs:
        cmap_kwargs["dark_mode"] = dark_mode

    grid_size = grid_size or 100
    xx, yy = np.mgrid[0:grid_size, 0:grid_size]

    legend_cmap = bivariate_from_params(
        values_a=xx,
        values_b=yy,
        mode=cmap_mode,
        params=cmap_params,
        **cmap_kwargs,
    )

    img = Image.fromarray(np.uint8((legend_cmap) * 255))

    label_a = label_a or parsed_values_a.name
    label_b = label_b or parsed_values_b.name

    tick_fontsize_pt = tick_fontsize_px * 72 / ax.figure.dpi

    colour = font_colour or ("white" if dark_mode else "black")
    _set_colour_theme(ax, colour)
    y_min = parsed_values_a.min()
    y_max = parsed_values_a.max()
    x_min = parsed_values_b.min()
    x_max = parsed_values_b.max()
    height_range = y_max - y_min
    width_range = x_max - x_min
    aspect = width_range / height_range
    ax.imshow(
        img,
        origin="lower",
        extent=(x_min, x_max, y_min, y_max) if tick_labels_a is None else None,
        aspect=aspect if tick_labels_a is None else None,
        interpolation="nearest",
    )
    ax.tick_params(axis="both", which="both", length=0)

    ax.annotate(
        "",
        xy=(0, 1),
        xytext=(0, 0),
        arrowprops=dict(
            arrowstyle="->",
            lw=1,
            color=colour,
            shrinkA=0,
            shrinkB=0,
        ),
        xycoords="axes fraction",
    )
    ax.annotate(
        "",
        xy=(1, 0),
        xytext=(0, 0),
        arrowprops=dict(
            arrowstyle="->",
            lw=1,
            color=colour,
            shrinkA=0,
            shrinkB=0,
        ),
        xycoords="axes fraction",
    )

    ax.set_ylabel(label_a, fontsize=tick_fontsize_pt)
    ax.set_xlabel(label_b, fontsize=tick_fontsize_pt)
    ax.tick_params(labelsize=tick_fontsize_pt)

    if tick_labels_a:
        yticks = np.linspace(-0.5, legend_cmap.shape[0] - 0.5, len(tick_labels_a))
        print(yticks)
        # xticks = np.arange(-0.5, cmap.shape[1], 1)
        # categorical
        # xticks = np.arange(0, cmap.shape[1], 1)
        ax.set_yticks(yticks)

        # ax.set_xticklabels(labels[:len(xticks)], ha="right")
        ax.set_yticklabels(tick_labels_a)
    # else:
    #     ax.yaxis.set_major_formatter(lambda y, pos: print(y, pos))

    if tick_labels_b:
        # labels = [0, *binning_start.bins]

        # numerical
        xticks = np.linspace(-0.5, legend_cmap.shape[1] - 0.5, len(tick_labels_b))
        print(xticks)
        # xticks = np.arange(-0.5, cmap.shape[1], 1)
        # categorical
        # xticks = np.arange(0, cmap.shape[1], 1)
        ax.set_xticks(xticks)

        # ax.set_xticklabels(labels[:len(xticks)], ha="right")
        ax.set_xticklabels(tick_labels_b)
    # else:
    # ax.xaxis.set_major_formatter(lambda x, pos: print(x, pos))


def _set_colour_theme(ax: Axes, colour: str) -> None:
    # ticks and tick labels
    ax.tick_params(axis="both", which="both", colors=colour)

    # axis labels and title
    ax.xaxis.label.set_color(colour)
    ax.yaxis.label.set_color(colour)

    # spines (borders)
    for spine in ax.spines.values():
        spine.set_visible(False)
