"""
Bivario.

Python library for plotting bivariate choropleth maps in Matplotlib and Folium.
"""

from bivario._folium import explore_bivariate_data
from bivario._legend import plot_bivariate_legend
from bivario.cmap import (
    bivariate_from_accents,
    bivariate_from_cmaps,
    bivariate_from_corners,
    bivariate_from_name,
    bivariate_from_params,
)

__app_name__ = "bivario"
__version__ = "0.1.0"

__all__ = [
    "bivariate_from_accents",
    "bivariate_from_cmaps",
    "bivariate_from_corners",
    "bivariate_from_name",
    "bivariate_from_params",
    "explore_bivariate_data",
    "plot_bivariate_legend",
]
