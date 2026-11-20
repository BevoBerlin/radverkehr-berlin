from datetime import datetime
from src.extract.zaehldaten import lese_zaehldaten, lese_standorte
from src.transform.zaehldaten import transformiere_zaehlung, transformiere_zaehlstelle

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