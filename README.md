# bivario
Python library for plotting bivariate choropleth maps in Matplotlib and Folium.

<p align="center">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/bivario_logo.png" width="500"><br/>
</p>

<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/raczeq/bivario?logo=mit&logoColor=%23fff">
    <img src="https://img.shields.io/github/checks-status/raczeq/bivario/main?logo=GitHubActions&logoColor=%23fff" alt="Checks">
    <a href="https://github.com/raczeq/bivario/actions/workflows/ci-prod.yml" target="_blank"><img alt="GitHub Workflow Status - PROD" src="https://img.shields.io/github/actions/workflow/status/raczeq/bivario/ci-prod.yml?label=build-prod&logo=GitHubActions&logoColor=%23fff"></a>
    <a href="https://results.pre-commit.ci/latest/github/raczeq/bivario/main" target="_blank"><img src="https://results.pre-commit.ci/badge/github/raczeq/bivario/main.svg" alt="pre-commit.ci status"></a>
    <a href="https://www.codefactor.io/repository/github/raczeq/bivario"><img alt="CodeFactor Grade" src="https://img.shields.io/codefactor/grade/github/raczeq/bivario?logo=codefactor&logoColor=%23fff"></a>
    <a href="https://app.codecov.io/gh/raczeq/bivario/tree/main"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/raczeq/bivario?logo=codecov&token=PRS4E02ZX0&logoColor=%23fff"></a>
    <a href="https://pypi.org/project/bivario" target="_blank"><img src="https://img.shields.io/pypi/v/bivario?color=%2334D058&label=pypi%20package&logo=pypi&logoColor=%23fff" alt="Package version"></a>
    <a href="https://pypi.org/project/bivario" target="_blank"><img src="https://img.shields.io/pypi/pyversions/bivario.svg?color=%2334D058&logo=python&logoColor=%23fff" alt="Supported Python versions"></a>
    <a href="https://pypi.org/project/bivario" target="_blank"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/bivario"></a>
</p>

# Installation

With pip:
```
pip install bivario
```

With uv:
```
uv add bivario
```

# Usage

<p align="center">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/bivario_combined.jpg"><br/>
  <span>Example of a Folium map in light and dark modes.</span>
</p>

Simple Folium map:

```python
from bivario import explore_bivariate_data
from bivario.example_data import nyc_bike_trips

explore_bivariate_data(
    nyc_bike_trips(), "morning_starts", "morning_ends"
)
```

In dark mode:

```python
from bivario import explore_bivariate_data
from bivario.example_data import nyc_bike_trips

explore_bivariate_data(
    nyc_bike_trips(),
    column_a="morning_starts",
    column_b="morning_ends",
    dark_mode=True, # default is False
)
```

Use other palette:

```python
from bivario import explore_bivariate_data
from bivario.example_data import nyc_bike_trips

explore_bivariate_data(
    nyc_bike_trips(),
    column_a="morning_starts",
    column_b="morning_ends",
    cmap="bubblegum"
)
```

Set numerical mode (disable bucketing):

> [!NOTE]
> By default, map is created using `Mapclassify` library with `NaturalBreaks` method to split data into 5 categories.
> Method and number of buckets can be changed or disabled completely.

```python
from bivario import explore_bivariate_data
from bivario.example_data import nyc_bike_trips

explore_bivariate_data(
    nyc_bike_trips(),
    column_a="morning_starts",
    column_b="morning_ends",
    dark_mode=True,
    cmap="late_sunset",
    scheme=False, # or set to None
    legend_size_px=300,
)
```

<p align="center">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/numeric_map.jpg"><br/>
  <span>Example of a Folium map in a numerical mode.</span>
</p>

# Bivariate colourmaps

Palettes in `bivario` are created by blending 2 or 4 colours in a 2D space using OKLab colour space. The operations on input and output are done in RGB, an internally are transformed into OKLab values using `colour-science` library.

`bivario` has 4 modes of Bivariate colourmaps:

**AccentsBivariateColourmap** - defined by two accent colours and a light and a dark colour.
<p align="left">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/accent_repr.png" height=200><br/>
</p>

**CornersBivariateColourmap** - defined by 4 corner colours (accent a/b, low value and high value)
<p align="left">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/corner_repr.png" height=200><br/>
</p>

**MplCmapBivariateColourmap** - defined by 2 Matplotlib colourmaps along axis X and Y
<p align="left">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/mpl_repr.png" height=200><br/>
</p>

**NamedBivariateColourmap** - can load predefined palette from string name
<p align="left">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/named_repr.png" height=200><br/>
</p>

## Available palettes

<p align="center">
  <img src="https://raw.githubusercontent.com/RaczeQ/bivario/main/images/available_palettes.png"><br/>
</p>

You can load these palettes by passing a string name to the `cmap` attribute, or load a `NamedBivariateColourmap` object:

```python
cmap = NamedBivariateColourmap("coral_ocean")

# You can call it similar to Matplotlib Colormap object
rgb_values = cmap(values_a=[0, 1], values_b=[0, 1])
```
