from dataclasses import dataclass

colour_tuple = tuple[float, float, float]


@dataclass
class BivariateCornerPalette:
    accent_a: colour_tuple
    accent_b: colour_tuple
    low: colour_tuple
    high: colour_tuple


BIVARIATE_CORNER_PALETTES = {
    "plum_mint": BivariateCornerPalette(
        accent_a=(0.66, 0.36, 0.80),
        accent_b=(0.07, 0.64, 0.58),
        low=(0.97, 0.94, 0.70),
        high=(0.12, 0.14, 0.40),
    ),
    "peacock_court": BivariateCornerPalette(
        accent_a=(0.58, 0.18, 0.70),
        accent_b=(0.10, 0.58, 0.66),
        low=(0.98, 0.97, 0.86),
        high=(0.10, 0.12, 0.22),
    ),
    "rosewood_pine": BivariateCornerPalette(
        accent_a=(0.88, 0.26, 0.60),
        accent_b=(0.07, 0.62, 0.40),
        low=(0.98, 0.96, 0.72),
        high=(0.14, 0.20, 0.36),
    ),
    "flamingo_lagoon": BivariateCornerPalette(
        accent_a=(0.96, 0.44, 0.60),
        accent_b=(0.14, 0.70, 0.56),
        low=(0.99, 0.98, 0.92),
        high=(0.12, 0.18, 0.22),
    ),
    "sunrise_harbor": BivariateCornerPalette(
        accent_a=(0.95, 0.40, 0.20),
        accent_b=(0.10, 0.62, 0.65),
        low=(0.98, 0.94, 0.60),
        high=(0.12, 0.18, 0.50),
    ),
    "coral_ocean": BivariateCornerPalette(
        accent_a=(0.94, 0.43, 0.46),
        accent_b=(0.06, 0.64, 0.68),
        low=(0.98, 0.95, 0.68),
        high=(0.12, 0.22, 0.42),
    ),
    "glacier_ember": BivariateCornerPalette(
        accent_a=(0.94, 0.48, 0.22),
        accent_b=(0.10, 0.48, 0.70),
        low=(1.00, 1.00, 0.98),
        high=(0.12, 0.14, 0.28),
    ),
    "verdant_orchard": BivariateCornerPalette(
        accent_a=(0.68, 0.28, 0.72),
        accent_b=(0.18, 0.72, 0.40),
        low=(0.98, 0.97, 0.72),
        high=(0.14, 0.16, 0.34),
    ),
    "frosted_marigold": BivariateCornerPalette(
        accent_a=(0.96, 0.62, 0.18),
        accent_b=(0.12, 0.56, 0.52),
        low=(0.99, 0.99, 0.96),
        high=(0.10, 0.12, 0.18),
    ),
    "marigold_current": BivariateCornerPalette(
        accent_a=(0.98, 0.58, 0.12),
        accent_b=(0.10, 0.52, 0.68),
        low=(0.99, 0.96, 0.70),
        high=(0.12, 0.18, 0.34),
    ),
    "amber_drift": BivariateCornerPalette(
        accent_a=(0.96, 0.50, 0.18),
        accent_b=(0.12, 0.46, 0.72),
        low=(0.99, 0.96, 0.64),
        high=(0.12, 0.16, 0.38),
    ),
    "triadic_garden": BivariateCornerPalette(
        accent_a=(0.66, 0.32, 0.82),
        accent_b=(0.94, 0.48, 0.18),
        low=(0.98, 0.97, 0.86),
        high=(0.14, 0.16, 0.34),
    ),
    "electric_neon": BivariateCornerPalette(
        accent_a=(0.12, 0.86, 0.78),
        accent_b=(0.94, 0.30, 0.34),
        low=(0.99, 0.97, 0.88),
        high=(0.14, 0.16, 0.32),
    ),
    "solar_pasture": BivariateCornerPalette(
        accent_a=(0.98, 0.74, 0.18),
        accent_b=(0.14, 0.66, 0.44),
        low=(0.99, 0.98, 0.90),
        high=(0.12, 0.16, 0.30),
    ),
    "jungle_roar": BivariateCornerPalette(
        accent_a=(0.96, 0.48, 0.16),
        accent_b=(0.12, 0.62, 0.38),
        low=(0.99, 0.97, 0.68),
        high=(0.08, 0.14, 0.12),
    ),
    "citrus_forest": BivariateCornerPalette(
        accent_a=(0.90, 0.50, 0.10),
        accent_b=(0.15, 0.65, 0.45),
        low=(0.95, 0.95, 0.60),
        high=(0.10, 0.15, 0.40),
    ),
    "berry_bush": BivariateCornerPalette(
        accent_a=(0.75, 0.20, 0.40),
        accent_b=(0.20, 0.60, 0.50),
        low=(0.95, 0.90, 0.85),
        high=(0.15, 0.15, 0.45),
    ),
    "late_sunset": BivariateCornerPalette(
        accent_a=(0.98, 0.56, 0.12),
        accent_b=(0.92, 0.20, 0.78),
        low=(0.99, 0.98, 0.92),
        high=(0.12, 0.16, 0.34),
    ),  # sherbet orange vs pastel plum; dessert-like, creamy baseline with gentle dark anchor
    "bubblegum": BivariateCornerPalette(
        accent_a=(0.10, 0.78, 0.86),
        accent_b=(0.94, 0.30, 0.56),
        low=(0.99, 0.96, 0.86),
        high=(0.14, 0.16, 0.34),
    ),  # electric aqua vs bubblegum magenta; carnival lights feel with soft luminous low
    "kaleidoscope": BivariateCornerPalette(
        accent_a=(0.12, 0.96, 0.82),
        accent_b=(0.96, 0.28, 0.54),
        low=(0.98, 0.72, 0.20),
        high=(0.46, 0.30, 0.96),
    ),  # neon teal, hot pink, citrine, electric indigo — high-energy kaleidoscope
    "radiant_shift": BivariateCornerPalette(
        accent_a=(0.98, 0.82, 0.28),
        accent_b=(0.78, 0.46, 0.86),
        low=(0.99, 0.98, 0.92),
        high=(0.36, 0.28, 0.92),
    ),  # brightness-led warm gold vs mid-light violet; one axis reads as bright→darker hue shifts
    "blade_runner": BivariateCornerPalette(
        accent_a=(0.10, 0.60, 0.70),
        accent_b=(0.96, 0.50, 0.18),
        low=(0.99, 0.97, 0.86),
        high=(0.14, 0.16, 0.34),
    ),  # cool neon-teal vs warm orange; high-contrast blockbuster grading for skin vs neon-lit environments
    "grand_budapest": BivariateCornerPalette(
        accent_a=(0.94, 0.56, 0.78),
        accent_b=(0.72, 0.36, 0.88),
        low=(0.99, 0.98, 0.96),
        high=(0.16, 0.12, 0.26),
    ),  # confectionery pastels and rose-plum; stylized period-piece color story
    "folk_warmth": BivariateCornerPalette(
        accent_a=(0.92, 0.56, 0.22),
        accent_b=(0.78, 0.46, 0.62),
        low=(0.99, 0.97, 0.90),
        high=(0.12, 0.14, 0.28),
    ),  # warm amber and soft rosewood; intimate, nostalgic drama tones
    "earth": BivariateCornerPalette(
        accent_a=(0.18, 0.56, 0.36),
        accent_b=(0.86, 0.66, 0.38),
        low=(0.99, 0.98, 0.90),
        high=(0.10, 0.12, 0.20),
    ),  # verdant greens vs warm ochres; terrestrial documentary naturalism with readable contrast
    "Library Ocean": BivariateCornerPalette(
        accent_a=(0.69, 0.85, 0.96),
        accent_b=(0.18, 0.56, 0.86),
        low=(0.96, 0.98, 0.99),
        high=(0.06, 0.22, 0.48),
    ),  # pale coastal aqua -> vibrant ocean blue; low = sunlit shallow, high = deep abyss indigo
    "Library Ocean Sunset": BivariateCornerPalette(
        accent_a=(0.66, 0.84, 0.94),
        accent_b=(0.18, 0.54, 0.86),
        low=(0.98, 0.88, 0.72),
        high=(0.06, 0.20, 0.46),
    ),  # pale sunset-wash (warm peach) over coastal aqua -> deep abyss indigo
    "Library Ocean Sunset (Warm Accents)": BivariateCornerPalette(
        accent_a=(0.98, 0.52, 0.18),
        accent_b=(0.86, 0.28, 0.60),
        low=(0.98, 0.88, 0.72),
        high=(0.06, 0.20, 0.46),
    ),  # warm orange and sunset magenta accents over peachy shallow -> abyss indigo
    "Library Ocean Sunset (Blue Accent, Softer Abyss)": BivariateCornerPalette(
        accent_a=(0.12, 0.56, 0.86),
        accent_b=(0.96, 0.48, 0.20),
        low=(0.98, 0.88, 0.72),
        high=(0.18, 0.36, 0.56),
    ),
    "Library Ocean Sunset (Sunset Accents, Blue Depths)": BivariateCornerPalette(
        accent_a=(0.98, 0.48, 0.12),
        accent_b=(0.12, 0.56, 0.86),
        low=(0.88, 0.94, 0.98),
        high=(0.20, 0.36, 0.60),
    ),
}
