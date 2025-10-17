from typing import TYPE_CHECKING, Any
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import geopandas as gpd
import narwhals as nw
from PIL import Image
import numpy as np

from bivario.cmap import (
    ALL_BIVARIATE_MODES_PARAMS,
    BIVARIATE_CMAP_MODES,
    bivariate_from_params,
    get_default_bivariate_params,
)

# fig, ax = plt.subplots(figsize=(IMG_SIZE_IN, IMG_SIZE_IN), dpi=DPI, constrained_layout=True)

if TYPE_CHECKING:
    from collections.abc import Iterable

    import numpy.typing as npt
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
    tick_fontsize_px=10,
) -> None:
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

    color = "white" if dark_mode else "black"
    with plt.rc_context(
        {
            "axes.labelcolor": color,
            "axes.edgecolor": color,
            "xtick.color": color,
            "ytick.color": color,
        }
    ):
        # lrbt
        ax.imshow(
            img,
            origin="lower",
            extent=(
                parsed_values_b.min(),
                parsed_values_b.max(),
                parsed_values_a.min(),
                parsed_values_a.max(),
            ),
        )
        ax.tick_params(axis="both", which="both", length=0)

        ax.annotate(
            "",
            xy=(0, 1),
            xytext=(0, 0),
            arrowprops=dict(
                arrowstyle="->",
                lw=1,
                color=color,
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
                color=color,
            ),
            xycoords="axes fraction",
        )

        ax.set_ylabel(label_a, fontsize=tick_fontsize_pt)
        ax.set_xlabel(label_b, fontsize=tick_fontsize_pt)
        ax.tick_params(labelsize=tick_fontsize_pt)

        if tick_labels_a:
            yticks = np.linspace(-0.5, legend_cmap.shape[2] - 0.5, len(tick_labels_a))
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
            # xticks = np.arange(-0.5, cmap.shape[1], 1)
            # categorical
            # xticks = np.arange(0, cmap.shape[1], 1)
            ax.set_xticks(xticks)

            # ax.set_xticklabels(labels[:len(xticks)], ha="right")
            ax.set_xticklabels(tick_labels_b)
        # else:
            # ax.xaxis.set_major_formatter(lambda x, pos: print(x, pos))
