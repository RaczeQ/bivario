"""Check that basic features work."""

if __name__ == "__main__":
    from bivario.cmap import bivariate_from_params
    from bivario.example_data import nyc_bike_trips

    dataset = nyc_bike_trips()

    cmap = bivariate_from_params(
        values_a=dataset["morning_starts"],
        values_b=dataset["morning_ends"],
        params="electric_neon",
    )

    if cmap.shape == (1569, 3):
        print("Smoke test succeeded")
    else:
        raise RuntimeError(f"Returned data has unexpected shape: {cmap.shape}")
