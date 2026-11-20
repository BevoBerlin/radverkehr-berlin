CODES = {"02-MI-AL-W": "01-MI-AL-W", "02-PA-SE-N": "11-PA-SE-N", "03-SP-NO-O": "16-SP-NO-O",
         "03-SP-NO-W": "16-SP-NO-W", "17-SK-BRE-O": "17-SZ-BRE-O", "17-SK-BRE-W": "17-SZ-BRE-W"}
FARBEN = {"theme5_0.4": "rekonstruiert", "FFFFEB9C": "keine_daten",
          "FFFFC000": "unplausibel", "theme7_0.6": "zeitumstellung"}
TYP = {"05-FK-OBB": "ausgehen", "21-NK-MAY": "ausgehen", "01-MI-AL": "pendeln", "03-MI-SAN": "pendeln"}

def transformiere_zaehlung(df):
    q = df.farbe.map(FARBEN).fillna("ok")
    q[(q == "ok") & df.anzahl.isna()] = "keine_daten"
    t = df.zeitpunkt
    q[t.dt.month.isin([3, 10]) & (t.dt.weekday == 6) & (t.dt.day > 24) & (t.dt.hour == 2)] = "zeitumstellung"
    return df.assign(zaehlstelle_code=df.zaehlstelle_code.replace(CODES),
                     anzahl=df.anzahl.astype("Int64"), qualitaet=q).drop(columns="farbe")

def transformiere_zaehlstelle(s):
    s = s.iloc[:, :2].set_axis(["zaehlstelle_code", "name"], axis=1)
    s["zaehlstelle_code"] = s.zaehlstelle_code.replace(CODES)
    s["standort_code"] = s.zaehlstelle_code.str.replace(r"-[NOSW]$", "", regex=True)
    s["streckentyp"] = s.standort_code.map(TYP)
    return s

