"""Typing aliases for bivario package."""

from collections.abc import Iterable
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from narwhals.typing import IntoSeries

NumericDType: TypeAlias = np.integer | np.floating | np.bool_
NumericArray: TypeAlias = npt.NDArray[NumericDType]
ValueInput: TypeAlias = IntoSeries | NumericArray | Iterable[float | int | bool]

BivariateColourmapArray: TypeAlias = npt.NDArray[np.floating]
