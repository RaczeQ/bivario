"""Bivariate legend plotting module."""

from contextlib import suppress
from typing import TYPE_CHECKING, Any, cast

import narwhals as nw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
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
    grid_size: int | tuple[int, int] | None = None,
    label_a: str | None = None,
    label_b: str | None = None,
    tick_labels_a: list[Any] | None = None,
    tick_labels_b: list[Any] | None = None,
    dark_mode: bool = False,
    font_colour: str | None = None,
    tick_fontsize_px: int = 10,
) -> Axes:
    """
    Plot bivariate 2D legend using Matplotlib.

    Generates a 2D matrix of values and uses imshow function to display it.

    Args:
        values_a (ValueInput): List or array of values for first variable.
            Will be assigned to the Y axis.
        values_b (ValueInput): List or array of values for second variable.
            Will be assigned to the X axis.
        ax (Axes | None, optional): Matplotlib axis to plot legend on. If None, will be created.
            Defaults to None.
        cmap (BivariateColourmap | str | None, optional): Bivariate colourmap to use.
            If None, will load a default one. Defaults to None.
        grid_size (int | tuple[int, int] | None, optional): Number of pixels in the legend grid.
            Can define two different values for X and Y axis (in this order).
            If None, will default to 100. Defaults to None.
        label_a (str | None, optional): Label to use for the first variable (Y axis).
            If None, will try to read series name, or defaults to "Value A".
            Defaults to None.
        label_b (str | None, optional): Label to use for the first variable (X axis).
            If None, will try to read series name, or defaults to "Value B".
            Defaults to None.
        tick_labels_a (list[Any] | None, optional): List of predefined ticks to use for the first
            variable (Y axis). Useful if binning has been applied. Defaults to None.
        tick_labels_b (list[Any] | None, optional): List of predefined ticks to use for the first
            variable (X axis). Useful if binning has been applied. Defaults to None.
        dark_mode (bool, optional): Whether to use dark mode to select a proper order of colours in
            the colourmap. Defaults to False.
        font_colour (str | None, optional): Font colour for the labels and ticks. If None, will be
            selected based on dark_mode value - white or black. Defaults to None.
        tick_fontsize_px (int, optional): Size of the ticksize and labels font in pixels.
            Defaults to 10.

    Returns:
        Axes: Matplotlib axes with plotted legend.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 8), dpi=DPI, layout="compressed")

    parsed_values_a, parsed_values_b = _validate_values(values_a, values_b)

    label_a = label_a or _try_parse_label(values_a) or "Value A"
    label_b = label_b or _try_parse_label(values_b) or "Value B"

    if isinstance(grid_size, (tuple, list)):
        grid_size_x, grid_size_y = grid_size
    else:
        grid_size_x = grid_size_y = grid_size or 100

    xx, yy = np.mgrid[0:grid_size_y, 0:grid_size_x]

    cmap = get_bivariate_cmap(cmap)

    legend_cmap = cmap(values_a=xx, values_b=yy, normalize=True, dark_mode=dark_mode)

    img = Image.fromarray(np.uint8((legend_cmap) * 255))

    tick_fontsize_pt = tick_fontsize_px * 72 / ax.figure.dpi

    colour = font_colour or ("white" if dark_mode else "black")
    _set_colour_theme(ax, colour)
    if tick_labels_a is None:
        y_min = parsed_values_a.min()
        y_max = parsed_values_a.max()
    else:
        y_min = 0
        y_max = legend_cmap.shape[0]

    if tick_labels_b is None:
        x_min = parsed_values_b.min()
        x_max = parsed_values_b.max()
    else:
        x_min = 0
        x_max = legend_cmap.shape[1]

    height_range = y_max - y_min
    width_range = x_max - x_min
    aspect = width_range / height_range

    ax.imshow(
        img,
        origin="lower",
        extent=(x_min, x_max, y_min, y_max),
        aspect=aspect,
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
        yticks = np.linspace(0, legend_cmap.shape[0], len(tick_labels_a))
        ax.set_yticks(yticks)
        ax.set_yticklabels(tick_labels_a)

    if tick_labels_b:
        xticks = np.linspace(0, legend_cmap.shape[1], len(tick_labels_b))
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


def resize_fig(fig: Figure, ax: Axes, legend_size_px: int, tolerance_px: float = 0.5) -> None:
    """Resize figure so that the Axes data area matches the target legend size in pixels."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    # Get bounding boxes (in display / pixel coordinates)
    bbox_ax = ax.get_window_extent(renderer)

    # Compute inner data area size (in pixels)
    data_width_px = bbox_ax.width
    data_height_px = bbox_ax.height

    max_tries = 1000
    total_tries = 0

    while (
        abs(legend_size_px - data_width_px) > tolerance_px
        or abs(legend_size_px - data_height_px) > tolerance_px
    ):
        if total_tries >= max_tries:
            w_in, h_in = fig.get_size_inches()
            raise RuntimeError(
                "Cannot resize fig to a given tolerance. "
                f"Current size: {w_in=} ({data_width_px=}), {h_in=} ({data_height_px=}). "
                f"Expected size: {legend_size_px=}."
            )
        # Calculate scale factor so data area = target_data_px
        width_scale = legend_size_px / data_width_px
        height_scale = legend_size_px / data_height_px

        # Compute new figure size (inches)
        w_in, h_in = fig.get_size_inches()
        new_w_in = w_in * width_scale
        new_h_in = h_in * height_scale

        fig.set_size_inches(new_w_in, new_h_in)

        auto_rotate_xticks(ax)

        # Redraw with new size
        fig.canvas.draw()

        renderer = fig.canvas.get_renderer()

        # Get bounding boxes (in display / pixel coordinates)
        bbox_ax = ax.get_window_extent(renderer)

        data_width_px = bbox_ax.width
        data_height_px = bbox_ax.height

        total_tries += 1
