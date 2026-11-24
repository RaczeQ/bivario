"""MapLibre basemap for Folium."""

from folium import TileLayer
from folium.elements import JSCSSMixin
from jinja2 import Template


class MapLibreLayer(JSCSSMixin, TileLayer):  # type: ignore[misc]
    """Basemap of a MapLibre style, drawn by MapLibre GL JS under the data of a Leaflet map."""

    _template = Template(
        """
            {% macro script(this,kwargs) %}
                var {{ this.get_name() }} = L.maplibreGL({style: {{ this.tiles|tojson }}});
                {{ this._parent.get_name() }}
                    .setMinZoom({{ this.min_zoom }}).setMaxZoom({{ this.max_zoom }});
            {% endmacro %}
            """
    )

    # The last major version of MapLibre GL JS that is not an ES module, as the plugin needs.
    default_js = [
        ("maplibre_gl", "https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.1/dist/maplibre-gl.js"),
        (
            "maplibre_gl_leaflet",
            "https://cdn.jsdelivr.net/npm/@maplibre/maplibre-gl-leaflet@0.1.4/leaflet-maplibre-gl.js",
        ),
    ]
    default_css = [
        ("maplibre_gl_css", "https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.1/dist/maplibre-gl.css"),
    ]

    def __init__(self, style: str, min_zoom: int = 0, max_zoom: int = 20) -> None:
        """
        Create a basemap.

        Args:
            style (str): URL of a MapLibre style.
            min_zoom (int, optional): Minimum zoom of the map. Defaults to 0.
            max_zoom (int, optional): Maximum zoom of the map. Defaults to 20.
        """
        # The attribution is read from the style by the plugin.
        super().__init__(tiles=style, attr=" ", name="Basemap")
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
