"""Show Lonboard maps as web pages: run in the kernels of the notebooks, as `PYTHONSTARTUP`."""

from IPython import get_ipython

formatter = get_ipython().display_formatter.formatters["text/html"]
formatter.for_type_by_name("lonboard._map", "Map", lambda map_: map_.to_html())
formatter.for_type_by_name(
    "bivario.lonboard", "LonboardMapWithLegend", lambda map_: map_.m.to_html()
)
