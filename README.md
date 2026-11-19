# Wettereinfluss auf den Radverkehr in Berlin

Abschlussprojekt der Data-Science-Weiterbildung (DBE Academy).
Das Projekt untersucht, wie stark Regen und Temperatur den Radverkehr in Berlin
beeinflussen, und vergleicht den Effekt zwischen Berufsverkehr und Ausgehnächten.

## Fragestellung und Hypothesen

- H1: Niederschlag und niedrige Temperaturen senken die stündliche Zahl der
  Radfahrenden, auch wenn Uhrzeit, Wochentag, Jahreszeit und Zählstelle
  berücksichtigt sind. (Alle Zählstellen)
- H2: Regen wirkt in den Ausgehnächten am Wochenende relativ schwächer als im
  morgendlichen Berufsverkehr. (Oberbaumbrücke, Maybachufer, Karl-Marx-Allee, Invalidenstraße)
- H3 (optional): Der Wettereffekt unterscheidet sich zwischen den Zählstellen.

Zeitraum: 2023–2025

## Datenquellen

Radverkehrszählungen
- Quelle: Senatsverwaltung für Mobilität, Verkehr, Klimaschutz und Umwelt, Berlin
- Datei: `gesamtdatei-stundenwerte.xlsx` (stündliche Zählwerte der Dauerzählstellen)
- Download: https://www.berlin.de/sen/uvk/_assets/verkehr/verkehrsplanung/radverkehr/weitere-radinfrastruktur/zaehlstellen-und-fahrradbarometer/gesamtdatei-stundenwerte.xlsx?ts=1782383913
- Abgerufen am: 14.11.2026
- Lizenz: Datenlizenz Deutschland – Zero – Version 2.0 (https://www.govdata.de/dl-de/zero-2-0)
- Hinweis: Die Daten wurden für dieses Projekt bearbeitet.

Wetterdaten
- Quelle: Deutscher Wetterdienst (DWD), abgerufen über die Bright-Sky-API
- (Details und Lizenzhinweis folgen beim Abruf)

## Rohdaten besorgen

Die Rohdaten sind nicht im Repository enthalten.
1. Die Excel-Datei über den Link oben herunterladen.
2. Unverändert unter `data/raw/` ablegen.


## Installation

1. Virtuelle Umgebung anlegen und aktivieren.
2. Pakete installieren: `python -m pip install -r requirements.txt`

## Projektstruktur

| Ordner | Inhalt |
|---|---|
| `data/raw` | Rohdaten (nicht in Git) |
| `data/processed` | bereinigte Daten (nicht in Git, werden vom ETL erzeugt) |
| `src/extract` | Daten einlesen und abrufen |
| `src/transform` | Daten bereinigen und umbauen |
| `src/load` | Daten in MySQL laden |
| `config` | Einstellungen (Jahre, Zählstellen, Schwellenwerte) |
| `sql` | Datenbankschema und Abfragen |
| `notebooks` | Analyse |
| `docs` | Dokumentation |
| `logs` | Protokolle der ETL-Läufe |

## Technik

Python, Pandas, MySQL (Docker), SQLAlchemy, statsmodels, Matplotlib, Jupyter, Git

## Stand

- [x] Projektstruktur, Git, Paketliste
- [ ] Datenbankschema
- [ ] ETL Zähldaten
- [ ] ETL Wetterdaten
- [ ] Analyse und Dashboard
- [ ] Präsentation