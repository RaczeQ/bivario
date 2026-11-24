"""Draw every palette to docs/palettes/ and write their page."""

from pathlib import Path

import basemaplibre as bml
import matplotlib.pyplot as plt
from mapclassify import NaturalBreaks
from matplotlib.colors import to_hex

from bivario import NamedBivariateColourmap, plot_bivariate_legend
from bivario.example_data import nyc_bike_trips
from bivario.palettes import BIVARIATE_CORNER_PALETTES

DOCS = Path(__file__).parent.parent / "docs"
EXTENT = (-74.03, -73.9, 40.69, 40.81)
MODES = {False: "OpenFreeMap.Positron", True: "OpenFreeMap.Dark"}
HEADER = """# Palettes

Pass a name to `cmap` of any function, or load it with `NamedBivariateColourmap`. The maps show \
where the morning trips of New York's bikes start and end, in the light and in the dark mode.
"""


def main() -> None:
    """Draw the palettes and write their page."""
    (DOCS / "palettes").mkdir(exist_ok=True)
    trips = nyc_bike_trips()
    starts = NaturalBreaks(trips["morning_starts"], k=5).yb
    ends = NaturalBreaks(trips["morning_ends"], k=5).yb
    page = HEADER
    for name, palette in BIVARIATE_CORNER_PALETTES.items():
        fig, axs = plt.subplots(1, 2, figsize=(10, 5.9), layout="constrained")
        for ax, (dark_mode, style) in zip(axs, MODES.items(), strict=True):
            cmap = NamedBivariateColourmap(name, dark_mode=dark_mode)
            ax.set_axis_off()
            ax.axis(EXTENT)
            trips.plot(ax=ax, color=cmap(starts, ends), alpha=0.8, edgecolor="none")
            ax.axis(EXTENT)
            bml.add_basemap(
                ax,
                crs=trips.crs,
                source=style,
                labels=False,
                attribution=None if dark_mode else False,
            )
            legend = ax.inset_axes((0.03, 0.71, 0.26, 0.26))
            plot_bivariate_legend(starts, ends, ax=legend, cmap=cmap, dark_mode=dark_mode)
            legend.set(xticks=[], yticks=[], xlabel="", ylabel="")
        fig.savefig(DOCS / "palettes" / f"{name}.webp", dpi=100, pil_kwargs={"quality": 85})
        plt.close(fig)
        colours = " ".join(f"`{to_hex(colour)}`" for colour in vars(palette).values())
        page += f"\n## {name}\n\n{colours}\n\n![{name}](palettes/{name}.webp)\n"
    (DOCS / "palettes.md").write_text(page)


if __name__ == "__main__":
    main()
