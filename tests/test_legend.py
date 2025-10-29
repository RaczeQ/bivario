"""Test legend plotting functionality."""

import pytest

from bivario.cmap import BivariateColourmap, NamedBivariateColourmap
from bivario.legend import plot_bivariate_legend


def test_plot_bivariate_legend() -> None:
    """Test that plot_bivariate_legend can be run without error."""
    plot_bivariate_legend(values_a=[0, 1], values_b=[0, 1])


def test_dark_mode_plotting() -> None:
    """Test that dark_mode can be set."""
    plot_bivariate_legend(values_a=[0, 1], values_b=[0, 1], dark_mode=True)


def test_different_font_size_plotting() -> None:
    """Test that font_size can be set."""
    plot_bivariate_legend(values_a=[0, 1], values_b=[0, 1], tick_fontsize_px=25)


@pytest.mark.parametrize("grid_size", [10, 64, 100, (3, 5), (3, 3), (100, 3), (5, 100), None])  # type: ignore
def test_different_grid_size_plotting(grid_size: int | tuple[int, int] | None) -> None:
    """Test that grid_size can be set."""
    ax = plot_bivariate_legend(values_a=[0, 1], values_b=[0, 1], grid_size=grid_size)
    img_data = ax.get_images()[0].get_array()
    assert img_data is not None, "No image data plotted on the array."

    expected_grid_size = (
        grid_size[::-1]
        if isinstance(grid_size, tuple)
        else (grid_size, grid_size)
        if grid_size is not None
        else (100, 100)
    )

    assert img_data.shape[:2] == expected_grid_size, "Mismatched image array size."


def test_different_tick_labels() -> None:
    """Test that tick_labels can be set."""
    plot_bivariate_legend(
        values_a=[0, 1],
        values_b=[0, 1],
        tick_labels_a=["A", "B", "C", "D"],
        tick_labels_b=["x", "y", "z"],
    )


def test_different_labels() -> None:
    """Test that labels can be set."""
    plot_bivariate_legend(
        values_a=[0, 1],
        values_b=[0, 1],
        label_a="A",
        label_b="B",
    )


@pytest.mark.parametrize("cmap", ["bubblegum", NamedBivariateColourmap("jungle_roar")])  # type: ignore
def test_different_cmap(cmap: BivariateColourmap | str) -> None:
    """Test that cmap can be set."""
    plot_bivariate_legend(values_a=[0, 1], values_b=[0, 1], cmap=cmap)


def test_mixed_axis() -> None:
    """Test that mixed grid size (continuous and distinct) can be set."""
    plot_bivariate_legend(
        values_a=[100, 150],
        values_b=[0, 1],
        tick_labels_b=["a", "b", "c", "d"],
        grid_size=(3, 100),
    )
