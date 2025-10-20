"""Test bivariate colormap functionality."""

import pytest

from bivario.cmap import ALL_BIVARIATE_MODES_PARAMS, BIVARIATE_CMAP_MODES


def test_bivariate_from_name_colourmap() -> None:
    """Test that bivariate_from_name can be run without error."""
    from bivario.cmap import bivariate_from_name

    bivariate_from_name(values_a=[0, 1], values_b=[0, 1], name="electric_neon")


def test_bivariate_from_cmaps_colourmap() -> None:
    """Test that bivariate_from_cmaps can be run without error."""
    from bivario.cmap import bivariate_from_cmaps

    bivariate_from_cmaps(values_a=[0, 1], values_b=[0, 1], cmap_a="Oranges", cmap_b="Blues")


def test_bivariate_from_accents_colourmap() -> None:
    """Test that bivariate_from_accents can be run without error."""
    from bivario.cmap import bivariate_from_accents

    bivariate_from_accents(
        values_a=[0, 1],
        values_b=[0, 1],
        accent_a=(0.95, 0.40, 0.20),
        accent_b=(0.10, 0.70, 0.65),
    )


def test_bivariate_from_corners_colourmap() -> None:
    """Test that bivariate_from_corners can be run without error."""
    from bivario.cmap import bivariate_from_corners

    bivariate_from_corners(
        values_a=[0, 1],
        values_b=[0, 1],
        accent_a=(0.95, 0.40, 0.20),
        accent_b=(0.10, 0.70, 0.65),
        low=(1.0, 1.0, 1.0),
        high=(0.0, 0.0, 0.0),
    )


@pytest.mark.parametrize(  # type: ignore[misc]
    "mode,params",
    [
        ("name", "electric_neon"),
        ("cmaps", ("Oranges", "Blues")),
        ("accents", ((0.95, 0.40, 0.20), (0.10, 0.70, 0.65))),
        ("corners", ((0.95, 0.40, 0.20), (0.10, 0.70, 0.65), (1.0, 1.0, 1.0), (0.0, 0.0, 0.0))),
    ],
)
def test_bivariate_from_params_colourmap(
    mode: BIVARIATE_CMAP_MODES, params: ALL_BIVARIATE_MODES_PARAMS
) -> None:
    """Test that bivariate_from_params can be run without error."""
    from bivario.cmap import bivariate_from_params

    bivariate_from_params(
        values_a=[0, 1],
        values_b=[0, 1],
        mode=mode,
        params=params,
    )


@pytest.mark.parametrize(  # type: ignore[misc]
    "params",
    [
        ("electric_neon"),
        (((0.95, 0.40, 0.20), (0.10, 0.70, 0.65), (1.0, 1.0, 1.0), (0.0, 0.0, 0.0))),
    ],
)
def test_bivariate_from_params_without_mode(params: ALL_BIVARIATE_MODES_PARAMS) -> None:
    """Test that bivariate_from_params can be run for corners and name."""
    from bivario.cmap import bivariate_from_params

    bivariate_from_params(
        values_a=[0, 1],
        values_b=[0, 1],
        params=params,
    )


def test_get_default_bivariate_params() -> None:
    """Test that get_default_bivariate_params can be run without error."""
    from bivario.cmap import get_default_bivariate_params

    for mode in ("accents", "cmaps", "corners", "name"):
        val = get_default_bivariate_params(mode)
        assert val is not None
