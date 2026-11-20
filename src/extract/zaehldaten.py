import openpyxl
import pandas as pd

DATEI = "data/raw/gesamtdatei-stundenwerte.xlsx"


def farbe(z):
    c = z.fill.fgColor
    if c.type == "theme":
        return f"theme{c.theme}_{c.tint:.1f}"
    return None if c.rgb == "00000000" else c.rgb


def lese_zaehldaten(jahre, datei=DATEI):
    wb = openpyxl.load_workbook(datei, read_only=True)
    daten = []
    for j in jahre:
        zeilen = wb[f"Jahresdatei {j}"].iter_rows()
        kopf = [str(z.value).split()[0] if z.value else None for z in next(zeilen)]
        for r in zeilen:
            for k, z in zip(kopf[1:], r[1:]):
                if k:
                    daten.append((r[0].value, k, None if z.value == "" else z.value, farbe(z)))
    wb.close()
    return pd.DataFrame(daten, columns=["zeitpunkt", "zaehlstelle_code", "anzahl", "farbe"])

def lese_standorte(datei=DATEI):
    return pd.read_excel(datei, sheet_name="Standortdaten")

if __name__ == "__main__":
    df = lese_zaehldaten([2023, 2024, 2025])
    print(df.shape, df.head(), df.groupby(df.zeitpunkt.dt.year).size(), df.farbe.value_counts(dropna=False), sep="\n\n")