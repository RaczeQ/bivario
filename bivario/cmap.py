"""
Bivariate colourmaps generators.

Returned values are in RGB colour space as floats in range from 0 to 1.

Colour operations are done in the OKLab colour space.
"""

import abc
import base64
import io
from typing import TYPE_CHECKING, Any, Literal

import narwhals as nw
import numpy as np
from colour import Oklab_to_XYZ, XYZ_to_Oklab, XYZ_to_sRGB, sRGB_to_XYZ
from matplotlib.colors import Colormap, rgb2hex, to_rgb
from matplotlib.pyplot import get_cmap
from matplotlib.typing import ColourType
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from bivario.palettes import BIVARIATE_CORNER_PALETTES

if TYPE_CHECKING:
    import numpy.typing as npt

    from bivario.typing import BivariateColourmapArray, NumericArray, ValueInput

NumericKinds = {"b", "i", "u", "f"}
_BIVAR_REPR_GRID_SIZE = 64
_BIVAR_REPR_PNG_SIZE = 256

__all__ = [
    "AccentsBivariateColourmap",
    "CornersBivariateColourmap",
    "MplCmapBivariateColourmap",
    "NamedBivariateColourmap",
    "get_bivariate_cmap",
]

BIVARIATE_CMAP_MODES = Literal["accents", "cmaps", "corners", "name"]

CMAPS_PARAMS = tuple[str | Colormap, str | Colormap]
CORNERS_PARAMS = tuple[ColourType, ColourType, ColourType, ColourType]
ACCENTS_PARAMS = tuple[ColourType, ColourType]
ALL_BIVARIATE_MODES_PARAMS = str | ACCENTS_PARAMS | CMAPS_PARAMS | CORNERS_PARAMS


class BivariateColourmap(abc.ABC):
    """Abstract class for Bivariate Colourmap object."""

    def __call__(
        self, values_a: "ValueInput", values_b: "ValueInput", normalize: bool = True, **kwargs: Any
    ) -> "BivariateColourmapArray":
        values_a, values_b = _validate_values(values_a, values_b)

        if normalize:
            values_a = _normalize_values(values_a)
            values_b = _normalize_values(values_b)

        return self._apply_colours(values_a=values_a, values_b=values_b, **kwargs)

    @abc.abstractmethod
    def _apply_colours(
        self, values_a: "NumericArray", values_b: "NumericArray", **kwargs: Any
    ) -> "BivariateColourmapArray":
        raise NotImplementedError

    def _repr_png_(self) -> bytes:
        """Generate a PNG representation of the Colormap."""
        from bivario import __version__

        xx, yy = np.mgrid[0:_BIVAR_REPR_GRID_SIZE, 0:_BIVAR_REPR_GRID_SIZE]

        cmap_arr = self(xx, yy)

        title = self.__str__()[1:-1]
        author = f"Bivario v{__version__}, https://github.com/RaczeQ/bivario/"
        pnginfo = PngInfo()
        pnginfo.add_text("Title", title)
        pnginfo.add_text("Description", title)
        pnginfo.add_text("Author", author)
        pnginfo.add_text("Software", author)

        png_bytes = io.BytesIO()

        Image.fromarray(np.uint8(cmap_arr * 255)).transpose(1).resize(
            size=(_BIVAR_REPR_PNG_SIZE, _BIVAR_REPR_PNG_SIZE)  # , resample=0
        ).save(png_bytes, format="png", pnginfo=pnginfo)

        return png_bytes.getvalue()

    def _repr_html_(self) -> str:
        """Generate an HTML representation of the Colormap."""
        png_bytes = self._repr_png_()
        png_base64 = base64.b64encode(png_bytes).decode("ascii")

        name = self.__str__()[1:-1]

        return (
            '<div style="vertical-align: middle;">'
            f"<strong>{name}</strong> "
            "</div>"
            '<div class="cmap"><img '
            f'alt="{name}" '
            f'title="{name}" '
            'style="border: 1px solid #555;" '
            f'src="data:image/png;base64,{png_base64}"></div>'
            '<div style="vertical-align: middle; '
            f"max-width: {_BIVAR_REPR_PNG_SIZE + 2}px; "
            'display: flex; justify-content: space-between;">'
            "</div>"
        )


class MplCmapBivariateColourmap(BivariateColourmap):
    """BivariateColourmap defined by 2 Matplotlib colourmaps."""

    def __init__(self, cmap_a: str | Colormap, cmap_b: str | Colormap) -> None:
        """
        Initialise MplCmapBivariateColourmap.

        Args:
            cmap_a (str | Colormap): First colourmap.
            cmap_b (str | Colormap): Second colourmap.
        """
        self.cmap_a = get_cmap(cmap_a)
        self.cmap_b = get_cmap(cmap_b)

    def __str__(self) -> str:
        """Full representation of the colourmap."""
        return f"<{self.__class__.__name__} ({self.cmap_a.name}, {self.cmap_b.name})>"

    def _apply_colours(
        self, values_a: "NumericArray", values_b: "NumericArray", **kwargs: Any
    ) -> "BivariateColourmapArray":
        va_colour = self.cmap_a(values_a)[..., :3]
        vb_colour = self.cmap_b(values_b)[..., :3]

        va_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(va_colour))
        vb_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(vb_colour))

        z_colour = np.zeros_like(va_colour, dtype=float)

        it = np.nditer(
            np.zeros(z_colour.shape[:-1]), flags=["multi_index"], op_flags=[["readwrite"]]
        )
        while not it.finished:
            pos_a, pos_b = values_a[it.multi_index], values_b[it.multi_index]

            loc_diff = pos_b - pos_a
            lerp_t = (loc_diff + 1) / 2

            colour_a = va_colour_oklab[it.multi_index]
            colour_b = vb_colour_oklab[it.multi_index]

            mixed_colour = _lerp(colour_a, colour_b, lerp_t)
            mixed_colour_rgb = np.clip(XYZ_to_sRGB(Oklab_to_XYZ(mixed_colour)), 0, 1)

            z_colour[it.multi_index] = mixed_colour_rgb
            it.iternext()

        return z_colour


class CornersBivariateColourmap(BivariateColourmap):
    """BivariateColourmap defined by 4 corners."""

    def __init__(
        self, accent_a: ColourType, accent_b: ColourType, low: ColourType, high: ColourType
    ) -> None:
        """
        Initialise CornersBivariateColourmap.

        Args:
            accent_a (ColourType): First colour accent.
            accent_b (ColourType): Second colour accent.
            low (ColourType): Low values colour.
            high (ColourType): High values colour.
        """
        self.a_colour = to_rgb(accent_a)
        self.b_colour = to_rgb(accent_b)
        self.low_colour = to_rgb(low)
        self.high_colour = to_rgb(high)

    def __str__(self) -> str:
        """Full representation of the colourmap."""
        return (
            f"<{self.__class__.__name__} (Accent A: {rgb2hex(self.a_colour)}, "
            f"Accent B: {rgb2hex(self.b_colour)}, Low: {rgb2hex(self.low_colour)}, "
            f"High: {rgb2hex(self.high_colour)})>"
        )

    def _apply_colours(
        self, values_a: "NumericArray", values_b: "NumericArray", **kwargs: Any
    ) -> "BivariateColourmapArray":
        z_colour = np.zeros((*values_a.shape, 3), dtype=float)

        a_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(self.a_colour)))
        b_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(self.b_colour)))
        low_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(self.low_colour)))
        high_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(self.high_colour)))

        it = np.nditer(
            np.zeros(z_colour.shape[:-1]), flags=["multi_index"], op_flags=[["readwrite"]]
        )
        while not it.finished:
            pos_a, pos_b = values_a[it.multi_index], values_b[it.multi_index]

            first_colour = _lerp(low_colour_oklab, a_colour_oklab, pos_a)
            second_colour = _lerp(b_colour_oklab, high_colour_oklab, pos_a)
            middle_colour = _lerp(first_colour, second_colour, pos_b)

            mixed_colour_rgb = np.clip(XYZ_to_sRGB(Oklab_to_XYZ(middle_colour)), 0, 1)

            z_colour[it.multi_index] = mixed_colour_rgb
            it.iternext()

        return z_colour


class NamedBivariateColourmap(BivariateColourmap):
    """BivariateColourmap loaded from predefined palettes."""

    def __init__(self, name: str, invert_accents: bool = False, dark_mode: bool = False) -> None:
        """
        Initialise NamedBivariateColourmap.

        Args:
            name (str): Name of the predefined palette.
            invert_accents (bool, optional): Whether to swap two colour accents.
                Can also be set during __call__. Defaults to False.
            dark_mode (bool, optional): Whether to use palette in dark mode.
                Swaps light and dark corners (low and high) for better readability on dark
                background. Can also be set during __call__. Defaults to False.
        """
        self.palette_name = name
        loaded_palette = BIVARIATE_CORNER_PALETTES.get(name)
        if loaded_palette is None:
            raise ValueError(
                f"Unrecognized palette: {name}. "
                f"Available palettes: {list(BIVARIATE_CORNER_PALETTES.keys())}."
            )

        self.accent_a, self.accent_b = loaded_palette.accent_a, loaded_palette.accent_b
        self.low, self.high = loaded_palette.low, loaded_palette.high
        self.invert_accents = invert_accents
        self.dark_mode = dark_mode

    def __str__(self) -> str:
        """Full representation of the colourmap."""
        return f"<{self.__class__.__name__} ({self.palette_name})>"

    def _apply_colours(
        self,
        values_a: "NumericArray",
        values_b: "NumericArray",
        invert_accents: bool | None = None,
        dark_mode: bool | None = None,
        **kwargs: Any,
    ) -> "BivariateColourmapArray":
        dark_mode = dark_mode if dark_mode is not None else self.dark_mode
        invert_accents = invert_accents if invert_accents is not None else self.invert_accents

        accent_a, accent_b = self.accent_a, self.accent_b

        if invert_accents:
            accent_a, accent_b = accent_b, accent_a

        low, high = self.low, self.high
        if dark_mode:
            low, high = high, low

        return CornersBivariateColourmap(
            accent_a=accent_a, accent_b=accent_b, low=low, high=high
        )._apply_colours(values_a, values_b)


class AccentsBivariateColourmap(BivariateColourmap):
    """BivariateColourmap defined by 2 colour accents."""

    def __init__(
        self,
        accent_a: ColourType,
        accent_b: ColourType,
        dark_mode: bool = False,
        light: ColourType | None = None,
        dark: ColourType | None = None,
    ) -> None:
        """
        Initialise AccentsBivariateColourmap.

        Args:
            accent_a (ColourType): First colour accent.
            accent_b (ColourType): Second colour accent.
            dark_mode (bool, optional): Whether to use palette in dark mode.
                Swaps light and dark corners (low and high) for better readability on dark
                background. Can also be set during __call__. Defaults to False.
            light (ColourType | None, optional): light corner colour.
                If None, will be (1, 1, 1). Defaults to None.
            dark (ColourType | None, optional): Dark corner colour.
                If None will be (0.15, 0.15, 0.15). Defaults to None.
        """
        self.accent_a = accent_a
        self.accent_b = accent_b
        self.light = light or (1, 1, 1)
        self.dark = dark or (0.15, 0.15, 0.15)
        self.dark_mode = dark_mode

    def __str__(self) -> str:
        """Full representation of the colourmap."""
        return (
            f"<{self.__class__.__name__} (Accent A: {rgb2hex(self.accent_a)}, "
            f"Accent B: {rgb2hex(self.accent_b)}, Light: {rgb2hex(self.light)}, "
            f"Dark: {rgb2hex(self.dark)})>"
        )

    def _apply_colours(
        self,
        values_a: "NumericArray",
        values_b: "NumericArray",
        dark_mode: bool | None = None,
        **kwargs: Any,
    ) -> "BivariateColourmapArray":
        dark_mode = dark_mode if dark_mode is not None else self.dark_mode

        accent_a, accent_b = self.accent_a, self.accent_b

        low = self.dark if dark_mode else self.light
        high = self.light if dark_mode else self.dark

        return CornersBivariateColourmap(
            accent_a=accent_a, accent_b=accent_b, low=low, high=high
        )._apply_colours(values_a, values_b)


def get_bivariate_cmap(cmap: str | BivariateColourmap | None = None) -> BivariateColourmap:
    """
    Return a BivariateColourmap object.

    Args:
        cmap (str | BivariateColourmap | None, optional): Colourmap name or object.
            If None, will load defalt named palette - rosewood_pine. Defaults to None.

    Raises:
        TypeError: If provided cmap object is of unknown type.

    Returns:
        BivariateColourmap: Parsed BivariateColourmap object.
    """
    # get the default color map
    if cmap is None:
        cmap = "rosewood_pine"

    # if the user passed in a BivariateColourmap, simply return it
    if isinstance(cmap, BivariateColourmap):
        return cmap
    if isinstance(cmap, str):
        return NamedBivariateColourmap(cmap)

    raise TypeError(
        "get_bivariate_cmap expects None or an instance of a str or BivariateColourmap. "
        f"you passed {cmap!r} of type {type(cmap)}"
    )


def _lerp(
    c_a: "npt.NDArray[np.floating]", c_b: "npt.NDArray[np.floating]", t: float
) -> "npt.NDArray[np.floating]":
    return (1 - t) * c_a + t * c_b


def _validate_values(
    values_a: "ValueInput", values_b: "ValueInput"
) -> "tuple[NumericArray, NumericArray]":
    values_a_array = _values_to_numpy(values_a)
    values_b_array = _values_to_numpy(values_b)

    if values_a_array.shape != values_b_array.shape:
        raise ValueError(
            f"Two arrays have different shape: {values_a_array.shape} vs {values_b_array.shape}."
        )

    return values_a_array, values_b_array


def _normalize_values(values: "NumericArray") -> "NumericArray":
    v_min: float = values.astype(float).min()
    v_max: float = values.astype(float).max()

    # Rescale values to fit into colourmap range (0->1)
    return (values - v_min) / (v_max - v_min)


def _values_to_numpy(values: "ValueInput") -> "NumericArray":
    try:
        values_array: np.ndarray = nw.from_native(values, series_only=True).to_numpy()
    except TypeError:
        values_array = np.array(values)

    _validate_numeric_noncomplex(values_array)

    return values_array


def _validate_numeric_noncomplex(arr: "npt.NDArray[Any]") -> None:
    if arr.dtype.kind not in NumericKinds:
        raise TypeError(
            f"unsupported dtype {arr.dtype}; only boolean/integer/unsigned/float allowed"
        )
    if np.issubdtype(arr.dtype, np.complexfloating):
        raise TypeError("complex dtypes are not allowed")
