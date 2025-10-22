"""Bivariate legend plotting module."""

from contextlib import suppress
from typing import TYPE_CHECKING, Any, cast

import narwhals as nw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from PIL import Image

from bivario.cmap import BivariateColourmap, _validate_values, get_bivariate_cmap

if TYPE_CHECKING:
    from bivario.typing import ValueInput

DPI = 100


def plot_bivariate_legend(
    values_a: "ValueInput",
    values_b: "ValueInput",
    ax: Axes | None = None,
    cmap: BivariateColourmap | str | None = None,
    grid_size: int | None = None,
    label_a: str | None = None,
    label_b: str | None = None,
    tick_labels_a: list[Any] | None = None,
    tick_labels_b: list[Any] | None = None,
    dark_mode: bool = False,
    font_colour: str | None = None,
    tick_fontsize_px: int = 10,
) -> Axes:
    if (tick_labels_a is not None and tick_labels_b is None) or (
        tick_labels_a is None and tick_labels_b is not None
    ):
        raise ValueError("Both tick labels for a and b values must be either None, or present.")

    if ax is None:
        _, ax = plt.subplots(figsize=(8, 8), dpi=DPI, layout="compressed")

    parsed_values_a, parsed_values_b = _validate_values(values_a, values_b)

    label_a = label_a or _try_parse_label(values_a) or "Value A"
    label_b = label_b or _try_parse_label(values_b) or "Value B"

    grid_size = grid_size or 100
    xx, yy = np.mgrid[0:grid_size, 0:grid_size]

    cmap = get_bivariate_cmap(cmap)

    legend_cmap = cmap(values_a=xx, values_b=yy, normalize=True, dark_mode=dark_mode)

    img = Image.fromarray(np.uint8((legend_cmap) * 255))

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
        ax.set_yticks(yticks)
        ax.set_yticklabels(tick_labels_a)

    if tick_labels_b:
        xticks = np.linspace(-0.5, legend_cmap.shape[1] - 0.5, len(tick_labels_b))
        ax.set_xticks(xticks)
        ax.set_xticklabels(tick_labels_b)
        auto_rotate_xticks(ax)

    return ax


def _try_parse_label(values: "ValueInput") -> str | None:
    with suppress(TypeError):
        return cast("str", nw.from_native(values, series_only=True).name)

    return None


def _set_colour_theme(ax: Axes, colour: str) -> None:
    # ticks and tick labels
    ax.tick_params(axis="both", which="both", colors=colour)

    # axis labels and title
    ax.xaxis.label.set_color(colour)
    ax.yaxis.label.set_color(colour)

    # spines (borders)
    for spine in ax.spines.values():
        spine.set_visible(False)


def auto_rotate_xticks(ax: Axes, rotation: float = 45) -> None:
    """Detect overlapping x-tick labels and rotate them if needed."""
    fig = ax.figure
    fig.canvas.draw()

    # Get bounding boxes of tick labels in display coords
    tick_labels = ax.get_xticklabels()
    bboxes = [label.get_window_extent() for label in tick_labels if label.get_text()]

    overlap = False
    for i in range(len(bboxes) - 1):
        if bboxes[i].overlaps(bboxes[i + 1]):
            overlap = True
            break

    if overlap:
        plt.setp(tick_labels, rotation=rotation, ha="right")
