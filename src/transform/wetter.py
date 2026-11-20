import pandas as pd


def transformiere_wetter(df):
    w = pd.DataFrame({
        "zeitpunkt": pd.to_datetime(df["timestamp"].str[:19]),
        "niederschlag_mm": df["precipitation"],
        "temperatur_c": df["temperature"],
        "wind_kmh": df["wind_speed"],
    })
    return w.drop_duplicates("zeitpunkt")