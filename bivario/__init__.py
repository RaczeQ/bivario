"""
Bivario.

Python library for plotting bivariate choropleth maps in Matplotlib and Folium.
"""

from bivario.cmap import (
    AccentsBivariateColourmap,
    CornersBivariateColourmap,
    MplCmapBivariateColourmap,
    NamedBivariateColourmap,
    get_bivariate_cmap,
)
from bivario.folium import explore_bivariate_data
from bivario.legend import plot_bivariate_legend

__app_name__ = "bivario"
__version__ = "0.2.0"

__all__ = [
    "AccentsBivariateColourmap",
    "CornersBivariateColourmap",
    "MplCmapBivariateColourmap",
    "NamedBivariateColourmap",
    "explore_bivariate_data",
    "get_bivariate_cmap",
    "plot_bivariate_legend",
]
