import requests
import pandas as pd

URL = "https://api.brightsky.dev/weather"


def lese_wetter(jahre):
    teile = []
    for j in jahre:
        p = {"dwd_station_id": "00433", "date": f"{j}-01-01",
             "last_date": f"{j + 1}-01-01", "tz": "Europe/Berlin"}
        r = requests.get(URL, params=p, timeout=60)
        r.raise_for_status()
        teile.append(pd.DataFrame(r.json()["weather"]))
    return pd.concat(teile, ignore_index=True)


if __name__ == "__main__":
    df = lese_wetter([2023])
    print(df.shape)
    print(df[["timestamp", "precipitation", "temperature", "wind_speed"]].head())