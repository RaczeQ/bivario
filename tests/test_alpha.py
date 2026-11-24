"""Test alpha values calculation."""

import numpy as np
import pytest

from bivario._alpha import prepare_alpha_values

RAMP = np.arange(11)
RAMP_ALPHA = np.sqrt(np.minimum(1, RAMP / 9))
ZEROS = np.zeros(11)


@pytest.mark.filterwarnings("error")  # type: ignore
@pytest.mark.parametrize(
    ("values_a", "values_b", "expected"),
    [
        (RAMP, RAMP, RAMP_ALPHA),
        # Columns of zeros do not change the alpha of the other one
        (ZEROS, RAMP, RAMP_ALPHA),
        (RAMP, ZEROS, RAMP_ALPHA),
        (ZEROS, ZEROS, ZEROS),
        # The quantile is 0, but not all of the values
        (RAMP == 10, ZEROS, RAMP == 10),
        (RAMP == 0, RAMP, np.where(RAMP == 0, 1, RAMP_ALPHA)),
        # Negative values
        (RAMP - 5, ZEROS, np.sqrt(np.clip((RAMP - 5) / 4, 0, 1))),
    ],
)  # type: ignore
def test_alpha_values(values_a: np.ndarray, values_b: np.ndarray, expected: np.ndarray) -> None:
    """Test that alpha values are always from 0 to 1."""
    alpha = prepare_alpha_values(values_a=values_a * 1.0, values_b=values_b * 1.0)

    np.testing.assert_allclose(alpha, expected)
