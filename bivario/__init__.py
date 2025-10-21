"""
Bivario.

Python library for plotting bivariate choropleth maps in Matplotlib and Folium.
"""

from bivario._folium import explore_bivariate_data
from bivario._legend import plot_bivariate_legend
from bivario.cmap import (
    AccentsBivariateColourmap,
    CornersBivariateColourmap,
    MplCmapBivariateColourmap,
    NamedBivariateColourmap,
    get_bivariate_cmap,
)

__app_name__ = "bivario"
__version__ = "0.1.0"

__all__ = [
    "AccentsBivariateColourmap",
    "CornersBivariateColourmap",
    "MplCmapBivariateColourmap",
    "NamedBivariateColourmap",
    "explore_bivariate_data",
    "get_bivariate_cmap",
    "plot_bivariate_legend",
]
