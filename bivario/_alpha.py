from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    import numpy.typing as npt

    from bivario.typing import NumericArray


def prepare_alpha_values(
    values_a: "NumericArray",
    values_b: "NumericArray",
    alpha_norm_quantile: float = 0.9,
) -> "npt.NDArray[np.float64]":
    if alpha_norm_quantile < 0 or alpha_norm_quantile > 1:
        raise ValueError("alpha_norm_quantile must be between 0 and 1 (inclusive).")

    alpha_values: npt.NDArray[np.float64] = np.sqrt(
        np.minimum(
            1,
            np.maximum(
                values_a / np.quantile(values_a, alpha_norm_quantile),
                values_b / np.quantile(values_b, alpha_norm_quantile),
            ),
        )
    ).astype(np.float64)

    return alpha_values
