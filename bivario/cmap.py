"""
Bivariate colourmaps generators.

Returned values are in RGB colour space as floats in range from 0 to 1.

Colour operations are done in the OKLab colour space.
"""

from typing import TYPE_CHECKING, Literal, cast

import narwhals as nw
import numpy as np
from colour import Oklab_to_XYZ, XYZ_to_Oklab, XYZ_to_sRGB, sRGB_to_XYZ
from matplotlib.colors import Colormap, to_rgb
from matplotlib.pyplot import get_cmap
from matplotlib.typing import ColourType

from bivario.palettes import BIVARIATE_CORNER_PALETTES

if TYPE_CHECKING:
    from collections.abc import Iterable

    import numpy.typing as npt
    from narwhals.typing import IntoSeries

    NumericDType = np.integer | np.floating | np.bool_
    NumericArray = npt.NDArray[NumericDType]
    ValueInput = IntoSeries | NumericArray | Iterable[NumericDType]

    BivariateColourmap = npt.NDArray[np.floating]

NumericKinds = {"b", "i", "u", "f"}

__all__ = [
    "bivariate_from_cmaps",
    "bivariate_from_accents",
    "bivariate_from_corners",
    "bivariate_from_name",
    "bivariate_from_params",
]

BIVARIATE_CMAP_MODES = Literal["accents", "cmaps", "corners", "name"]

CMAPS_PARAMS = tuple[str | Colormap, str | Colormap]
CORNERS_PARAMS = tuple[ColourType, ColourType, ColourType, ColourType]
ACCENTS_PARAMS = tuple[ColourType, ColourType]
ALL_BIVARIATE_MODES_PARAMS = str | ACCENTS_PARAMS | CMAPS_PARAMS | CORNERS_PARAMS


def bivariate_from_params(
    values_a: "ValueInput",
    values_b: "ValueInput",
    params: ALL_BIVARIATE_MODES_PARAMS,
    mode: BIVARIATE_CMAP_MODES | None = None,
    **kwargs,
) -> "BivariateColourmap":
    """Generate a 2D bivariate palette."""
    # can operate on all other functions, used for API usage

    # match types first - detect corners and name
    if isinstance(params, str):
        name = params
        return bivariate_from_name(values_a=values_a, values_b=values_b, name=name, **kwargs)
    # detected corners
    elif len(params) == 4:
        accent_a, accent_b, low, high = params
        return bivariate_from_corners(
            values_a=values_a,
            values_b=values_b,
            accent_a=accent_a,
            accent_b=accent_b,
            low=low,
            high=high,
        )

    match mode:
        case "accents":
            accent_a, accent_b = cast("ACCENTS_PARAMS", params)
            return bivariate_from_accents(
                values_a=values_a, values_b=values_b, accent_a=accent_a, accent_b=accent_b, **kwargs
            )
        case "cmaps":
            cmap_a, cmap_b = cast("CMAPS_PARAMS", params)
            return bivariate_from_cmaps(
                values_a=values_a, values_b=values_b, cmap_a=cmap_a, cmap_b=cmap_b, **kwargs
            )
        case "corners":
            accent_a, accent_b, low, high = cast("CORNERS_PARAMS", params)
            return bivariate_from_corners(
                values_a=values_a,
                values_b=values_b,
                accent_a=accent_a,
                accent_b=accent_b,
                low=low,
                high=high,
            )
        case "name":
            name = cast("str", params)
            return bivariate_from_name(values_a=values_a, values_b=values_b, name=name, **kwargs)

        case _:
            raise ValueError(f"Unknown bivariate cmap mode: '{mode}'.")


def get_default_bivariate_params(mode: BIVARIATE_CMAP_MODES) -> ALL_BIVARIATE_MODES_PARAMS:
    match mode:
        case "accents":
            accent_a = (0.95, 0.40, 0.20)
            accent_b = (0.10, 0.70, 0.65)
            return (accent_a, accent_b)
        case "cmaps":
            return ("Oranges", "Blues")
        case "corners":
            loaded_palette = BIVARIATE_CORNER_PALETTES["electric_neon"]
            return (
                loaded_palette.accent_a,
                loaded_palette.accent_b,
                loaded_palette.low,
                loaded_palette.high,
            )
        case "name":
            return "electric_neon"

        case _:
            raise ValueError(f"Unknown bivariate cmap mode: '{mode}'.")


def bivariate_from_cmaps(
    values_a: "ValueInput",
    values_b: "ValueInput",
    cmap_a: str | Colormap,
    cmap_b: str | Colormap,
) -> "BivariateColourmap":
    """Blend two 1D colourmaps into a 2D bivariate palette."""
    _values_a, _values_b = _validate_values(values_a, values_b)

    va_plot = _normalize_values(_values_a)
    vb_plot = _normalize_values(_values_b)

    cmap_a = get_cmap(cmap_a)
    cmap_b = get_cmap(cmap_b)

    va_colour = cmap_a(va_plot)[..., :3]
    vb_colour = cmap_b(vb_plot)[..., :3]

    va_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(va_colour))
    vb_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(vb_colour))

    z_colour = np.zeros_like(va_colour)

    it = np.nditer(np.zeros(z_colour.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        pos_a, pos_b = va_plot[it.multi_index], vb_plot[it.multi_index]

        loc_diff = pos_b - pos_a
        lerp_t = (loc_diff + 1) / 2

        colour_a = va_colour_oklab[it.multi_index]
        colour_b = vb_colour_oklab[it.multi_index]

        mixed_colour = _lerp(colour_a, colour_b, lerp_t)
        mixed_colour_rgb = np.clip(XYZ_to_sRGB(Oklab_to_XYZ(mixed_colour)), 0, 1)

        z_colour[it.multi_index] = mixed_colour_rgb
        it.iternext()

    return z_colour


def bivariate_from_corners(
    values_a: "ValueInput",
    values_b: "ValueInput",
    accent_a: ColourType,
    accent_b: ColourType,
    low: ColourType,
    high: ColourType,
    # accent_a=(0.95, 0.40, 0.20),
    # accent_b=(0.10, 0.70, 0.65),
    # low=(0.95, 0.85, 0.55),
    # high=(0.15, 0.20, 0.50),
) -> "BivariateColourmap":
    """Generate a 2D bivariate palette from four RGB values."""
    _values_a, _values_b = _validate_values(values_a, values_b)

    va_plot = _normalize_values(_values_a)
    vb_plot = _normalize_values(_values_b)

    z_colour = np.zeros((*va_plot.shape, 3))

    a_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(to_rgb(accent_a))))
    b_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(to_rgb(accent_b))))
    low_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(to_rgb(low))))
    high_colour_oklab = XYZ_to_Oklab(sRGB_to_XYZ(np.array(to_rgb(high))))

    it = np.nditer(np.zeros(z_colour.shape[:-1]), flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        pos_a, pos_b = va_plot[it.multi_index], vb_plot[it.multi_index]

        first_colour = _lerp(low_colour_oklab, a_colour_oklab, pos_a)
        second_colour = _lerp(b_colour_oklab, high_colour_oklab, pos_a)
        middle_colour = _lerp(first_colour, second_colour, pos_b)

        mixed_colour_rgb = np.clip(XYZ_to_sRGB(Oklab_to_XYZ(middle_colour)), 0, 1)

        z_colour[it.multi_index] = mixed_colour_rgb
        it.iternext()

    return z_colour


def bivariate_from_accents(
    values_a: "ValueInput",
    values_b: "ValueInput",
    accent_a: ColourType,
    accent_b: ColourType,
    *,
    dark_mode=False,
    light: ColourType = (1, 1, 1),
    dark: ColourType = (0.15, 0.15, 0.15),
) -> "BivariateColourmap":
    """Blend two accent colours into a 2D bivariate palette."""
    if dark_mode:
        return bivariate_from_corners(values_a, values_b, accent_a, accent_b, low=dark, high=light)

    return bivariate_from_corners(values_a, values_b, accent_a, accent_b, low=light, high=dark)


def bivariate_from_name(
    values_a: "ValueInput",
    values_b: "ValueInput",
    name: str,
    dark_mode=False,
    invert_accents: bool = False,
) -> "BivariateColourmap":
    """Load bivariate palette from name."""
    loaded_palette = BIVARIATE_CORNER_PALETTES.get(name)
    if loaded_palette is None:
        raise ValueError(
            f"Unrecognized palette: {name}. "
            f"Available palettes: {list(BIVARIATE_CORNER_PALETTES.keys())}."
        )

    accent_a, accent_b = loaded_palette.accent_a, loaded_palette.accent_b
    if invert_accents:
        accent_a, accent_b = accent_b, accent_a

    low, high = loaded_palette.low, loaded_palette.high
    if dark_mode:
        low, high = high, low

    return bivariate_from_corners(
        values_a=values_a,
        values_b=values_b,
        accent_a=accent_a,
        accent_b=accent_b,
        low=low,
        high=high,
    )


def _lerp(c_a, c_b, t):
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
    v_min = values.min()
    v_max = values.max()

    # Rescale values to fit into colourmap range (0->1)
    return (values - v_min) / (v_max - v_min)


def _values_to_numpy(values: "ValueInput") -> "NumericArray":
    try:
        values_array = nw.from_native(values, series_only=True).to_numpy()
    except TypeError:
        values_array = np.array(values)

    _validate_numeric_noncomplex(values_array)

    return values_array


def _validate_numeric_noncomplex(arr: "npt.NDArray") -> None:
    if arr.dtype.kind not in NumericKinds:
        raise TypeError(
            f"unsupported dtype {arr.dtype}; only boolean/integer/unsigned/float allowed"
        )
    if np.issubdtype(arr.dtype, np.complexfloating):
        raise TypeError("complex dtypes are not allowed")
