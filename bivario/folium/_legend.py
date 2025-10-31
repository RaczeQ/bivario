"""Custom Folium HTML object."""

import base64
import io
from typing import Any, Literal

from branca.element import MacroElement
from folium.template import Template
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from bivario.legend import DPI, resize_fig


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
    ) -> None:
        """
        Create a floating bivariate legend for folium maps.

        Args:
            fig (Figure): Matplotlib figure containing the legend.
            ax (Axes): Matplotlib axes containing the legend.
            legend_size_px (int): Size of the legend in pixels.
            legend_loc (Literal["bl", "br", "tl", "tr"] | None, optional): Location of the legend
                on the map. Can be "bl" (bottom-left), "br" (bottom-right), "tl" (top-left),
                or "tr" (top-right). Defaults to "bl".
            legend_offset_px (float | tuple[float, float] | None, optional): Offset of the legend
                from the specified location in pixels. If None, uses default offsets based on
                location. Defaults to None.
            legend_background (bool, optional): Whether to add a background to the legend.
                Defaults to True.
            legend_border (bool, optional): Whether to add a border to the legend.
                Defaults to True.
            padding_top_right_corner (bool, optional): Whether to add padding for top-right
                legend corner for readabilty. Defaults to False.
            **kwargs (Any): Additional CSS properties for the legend.
        """
        super().__init__()
        self._name = FloatBivariateMatplotlibLegend.__name__

        self.css = kwargs

        if legend_background:
            self.css["background"] = "rgba(255, 255, 255, 0.8)"
            self.css["padding"] = "2px" if padding_top_right_corner else "0 0 2px 2px"

            if legend_border:
                self.css["border"] = "2px solid rgba(0, 0, 0, 0.2)"
                self.css["border-radius"] = "4px"
                self.css["background-clip"] = "padding-box"

        resize_fig(fig=fig, ax=ax, legend_size_px=legend_size_px)

        self.image = "data:image/svg+xml;base64," + self.figure_to_base64_string(fig)

        plt.close()

        self.css.pop("bottom", None)
        self.css.pop("top", None)
        self.css.pop("left", None)
        self.css.pop("right", None)
        self.css.pop("transform", None)

        legend_loc = legend_loc or "bl"

        match legend_loc:
            case "bl":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (5, 40)
                )
                self.css["bottom"] = f"{legend_position_y}px"
                self.css["left"] = f"{legend_position_x}px"
            case "br":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (5, 19)
                )
                self.css["bottom"] = f"{legend_position_y}px"
                self.css["right"] = f"{legend_position_x}px"
            case "tl":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (10, 79)
                )
                self.css["top"] = f"{legend_position_y}px"
                self.css["left"] = f"{legend_position_x}px"
            case "tr":
                legend_position_x, legend_position_y = self.parse_offset(
                    legend_offset_px or (10, 10)
                )
                self.css["top"] = f"{legend_position_y}px"
                self.css["right"] = f"{legend_position_x}px"

    def figure_to_base64_string(self, fig: Figure) -> str:
        """Convert Matplotlib figure to base64-encoded SVG string."""
        buffered = io.BytesIO()
        fig.savefig(
            buffered, format="svg", transparent=True, dpi=DPI, bbox_inches="tight", pad_inches=0
        )
        return base64.b64encode(buffered.getvalue()).decode("ascii")

    def parse_offset(self, legend_offset_px: float | tuple[float, float]) -> tuple[float, float]:
        """Parse legend offset into x and y components."""
        if isinstance(legend_offset_px, (int, float)):
            legend_position_x = legend_position_y = legend_offset_px
        else:
            legend_position_x, legend_position_y = legend_offset_px
        return (legend_position_x, legend_position_y)
