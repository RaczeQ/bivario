"""Typing aliases for bivario package."""

from collections.abc import Iterable
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from narwhals.series import Series
from narwhals.typing import IntoSeries

NumericDType: TypeAlias = np.integer | np.floating | np.bool_
NumericArray: TypeAlias = npt.NDArray[NumericDType]
ValueInput: TypeAlias = Series | IntoSeries | NumericArray | Iterable[float | int | bool]

BivariateColourmapArray: TypeAlias = npt.NDArray[np.floating]
