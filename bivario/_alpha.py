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

    # A quantile can be equal to 0, then zeros (0 / 0) are transparent and higher values are opaque.
    with np.errstate(divide="ignore", invalid="ignore"):
        ratios = np.fmax(
            values_a / np.quantile(values_a, alpha_norm_quantile),
            values_b / np.quantile(values_b, alpha_norm_quantile),
        )

    alpha_values: npt.NDArray[np.float64] = np.sqrt(np.nan_to_num(np.clip(ratios, 0, 1))).astype(
        np.float64
    )

    return alpha_values
