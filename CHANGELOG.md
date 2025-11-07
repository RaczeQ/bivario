# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Matplotlib example notebook
- Option to pass `**kwargs` to `get_bivariate_cmap` function

## [0.3.0] - 2025-10-31

### Added

- Lonboard plotting support with `bivario.lonboard.viz_bivariate_data` [#11](https://github.com/RaczeQ/bivario/issues/11)
- Support for mixing different `scheme` and `k` values for mapclassify as well as mixing continuous and distinct values [#12](https://github.com/RaczeQ/bivario/issues/12)

### Changed

- Removed `GeoPandas` and `folium` from required dependencies.
- Lowered required dependencies versions:
  - colour-science>=0.4.0
  - mapclassify>=2
  - matplotlib>=3.3
  - narwhals>=1.9.4
  - numpy>=1.19

## [0.2.0] - 2025-10-22

### Added

- Dedicated `AccentsBivariateColourmap`, `CornersBivariateColourmap`, `MplCmapBivariateColourmap` and `NamedBivariateColourmap` classes

### Changed

- Bivariate Colourmaps API
- Example data format from `.parquet` to `.csv.gz`

## [0.1.0] - 2025-10-20

### Added

- Colourmaps generation functionality
- Matplotlib legend plotting functionality
- Folium plotting functionality

[Unreleased]: https://github.com/RaczeQ/bivario/compare/0.3.0...HEAD

[0.3.0]: https://github.com/RaczeQ/bivario/compare/0.2.0...0.3.0

[0.2.0]: https://github.com/RaczeQ/bivario/compare/0.1.0...0.2.0

[0.1.0]: https://github.com/RaczeQ/bivario/releases/tag/0.1.0
