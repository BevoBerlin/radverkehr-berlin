import holidays
import pandas as pd
from datetime import datetime
from src.extract.zaehldaten import lese_zaehldaten, lese_standorte
from src.transform.zaehldaten import transformiere_zaehlung, transformiere_zaehlstelle
from src.extract.wetter import lese_wetter
from src.transform.wetter import transformiere_wetter

JAHRE = [2023, 2024, 2025]

z = transformiere_zaehlung(lese_zaehldaten(JAHRE))
s = transformiere_zaehlstelle(lese_standorte())

assert not z.duplicated(["zaehlstelle_code", "zeitpunkt"]).any()
assert z.zaehlstelle_code.isin(s.zaehlstelle_code).all()

v = z.qualitaet.value_counts()
print(s, z.head(), v, sep="\n\n")

s.to_csv("data/processed/zaehlstelle.csv", index=False)
z.to_csv("data/processed/zaehlung.csv", index=False)
with open("logs/etl.log", "a") as f:
    f.write(f"{datetime.now():%Y-%m-%d %H:%M} Zaehldaten {JAHRE}: {len(s)} Zaehlstellen, {len(z)} Zeilen, {v.to_dict()}\n")

roh = lese_wetter(JAHRE)
wetter = transformiere_wetter(roh)
doppelt = len(roh) - len(wetter)
fb = roh.filter(like="fallback").notna().sum().sum()
zeiten = z["zeitpunkt"].drop_duplicates() + pd.Timedelta(hours=1)
fehlt = (~zeiten.isin(wetter["zeitpunkt"])).sum()
print(len(roh), len(wetter), doppelt, roh["source_id"].unique(), fb, fehlt)
print(wetter.isna().sum())
wetter.to_csv("data/processed/wetter.csv", index=False)
with open("logs/etl.log", "a", encoding="utf-8") as f:
    f.write(f"{datetime.now():%Y-%m-%d %H:%M} wetter: {len(wetter)} Zeilen, {doppelt} doppelt, "
            f"Quellen {list(roh['source_id'].unique())}, Fallback {fb}, ohne Wetter {fehlt}\n")

feiertag = pd.DataFrame(sorted(holidays.Germany(subdiv="BE", years=JAHRE).items()),
                        columns=["datum", "name"])
print(len(feiertag))
feiertag.to_csv("data/processed/feiertag.csv", index=False)
with open("logs/etl.log", "a", encoding="utf-8") as f:
    f.write(f"{datetime.now():%Y-%m-%d %H:%M} feiertag: {len(feiertag)} Zeilen\n")