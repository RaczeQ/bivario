"""Test bivariate colormap functionality."""


def test_default_bivariate_colourmap() -> None:
    """Test that NamedBivariateColourmap can be run without error."""
    from bivario import get_bivariate_cmap

    cmap = get_bivariate_cmap()
    cmap(values_a=[0, 1], values_b=[0, 1])


def test_bivariate_from_name_colourmap() -> None:
    """Test that NamedBivariateColourmap can be run without error."""
    from bivario import NamedBivariateColourmap

    cmap = NamedBivariateColourmap("rosewood_pine")
    cmap(values_a=[0, 1], values_b=[0, 1])


def test_bivariate_from_cmaps_colourmap() -> None:
    """Test that MplCmapBivariateColourmap can be run without error."""
    from bivario import MplCmapBivariateColourmap

    cmap = MplCmapBivariateColourmap(cmap_a="Oranges", cmap_b="Blues")
    cmap(values_a=[0, 1], values_b=[0, 1])


def test_bivariate_from_accents_colourmap() -> None:
    """Test that AccentsBivariateColourmap can be run without error."""
    from bivario import AccentsBivariateColourmap

    cmap = AccentsBivariateColourmap(accent_a=(0.95, 0.40, 0.20), accent_b=(0.10, 0.70, 0.65))
    cmap(values_a=[0, 1], values_b=[0, 1])


def test_bivariate_from_corners_colourmap() -> None:
    """Test that CornersBivariateColourmap can be run without error."""
    from bivario import CornersBivariateColourmap

    cmap = CornersBivariateColourmap(
        accent_a=(0.95, 0.40, 0.20),
        accent_b=(0.10, 0.70, 0.65),
        low=(1.0, 1.0, 1.0),
        high=(0.0, 0.0, 0.0),
    )
    cmap(values_a=[0, 1], values_b=[0, 1])
