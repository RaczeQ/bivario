from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from mapclassify import classify
from mapclassify.classifiers import _format_intervals

if TYPE_CHECKING:
    from mapclassify.classifiers import MapClassifier

    from bivario.typing import NumericArray


SCHEME_TYPE = str | None | bool


@dataclass
class MapclassifyResult:
    values_a: "NumericArray"
    values_b: "NumericArray"
    tick_labels_a: list[str] | None
    tick_labels_b: list[str] | None
    scheme_a: str | None
    scheme_b: str | None
    k_a: int
    k_b: int


def apply_mapclassify(
    values_a: "NumericArray",
    values_b: "NumericArray",
    scheme: SCHEME_TYPE | tuple[SCHEME_TYPE, SCHEME_TYPE] = True,
    k: int | tuple[int, int] = 5,
) -> MapclassifyResult:
    tick_labels_a = None
    tick_labels_b = None

    if isinstance(scheme, (tuple, list)):
        scheme_a, scheme_b = scheme
    else:
        scheme_a = scheme_b = scheme

    if isinstance(k, (tuple, list)):
        k_a, k_b = k
    else:
        k_a = k_b = k

    if isinstance(scheme_a, bool):
        scheme_a = "NaturalBreaks" if scheme_a else None
    if isinstance(scheme_b, bool):
        scheme_b = "NaturalBreaks" if scheme_b else None

    if scheme_a is not None:
        binning_a = cast("MapClassifier", classify(values_a, scheme=scheme_a, k=k_a))
        values_a = binning_a.yb
        tick_labels_a = [_l.replace(".0", "") for _l in _format_intervals(binning_a, "{:,.1f}")[0]]

    if scheme_b is not None:
        binning_b = cast("MapClassifier", classify(values_b, scheme=scheme_b, k=k_b))
        values_b = binning_b.yb
        tick_labels_b = [_l.replace(".0", "") for _l in _format_intervals(binning_b, "{:,.1f}")[0]]

    return MapclassifyResult(
        values_a=values_a,
        values_b=values_b,
        tick_labels_a=tick_labels_a,
        tick_labels_b=tick_labels_b,
        scheme_a=scheme_a,
        scheme_b=scheme_b,
        k_a=k_a,
        k_b=k_b,
    )
