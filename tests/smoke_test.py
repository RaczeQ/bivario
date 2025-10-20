"""Check that basic features work."""

from bivario.cmap import bivariate_from_params

bivariate_from_params(
    values_a=[0, 1],
    values_b=[0, 1],
    params="electric_neon",
)

# TODO: check example file content
