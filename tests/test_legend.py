"""Test legend plotting functionality."""


def test_plot_bivariate_legend() -> None:
    """Test that plot_bivariate_legend can be run without error."""
    from bivario.legend import plot_bivariate_legend

    plot_bivariate_legend(values_a=[0, 1], values_b=[0, 1])
