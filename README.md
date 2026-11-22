# Wettereinfluss auf den Radverkehr in Berlin

Abschlussprojekt der Data Science Weiterbildung. Untersucht wird, wie stark Regen, Temperatur und Wind den Radverkehr in Berlin beeinflussen und ob Nachtschwärmer anders auf Regen reagieren als Pendler. Datengrundlage sind stündliche Werte der Berliner Radzählstellen und der DWD-Wetterstation Berlin-Tempelhof für 2023–2025.

## Ergebnisse auf einen Blick

| Frage | Ergebnis |
|---|---|
| **H1:** Senken Regen und Kälte den Radverkehr? | **Ja.** Regen: −29 % (ab 0,5 mm: −34 %), je °C wärmer: +2,9 %, je km/h Wind: −0,6 % |
| **H2:** Ist der Regeneffekt in Ausgehnächten schwächer als im Berufsverkehr? | **Nein.** Ausgehnacht −33 %, Berufsverkehr −30 % (Unterschied nicht gesichert) |
| Robustheit | Ergebnis stabil ohne rekonstruierte Werte; Regen wirkt in der Folgestunde nach (−20 %) |

Details, Diagramme und Grenzen der Analyse: [`notebooks/analyse.ipynb`](notebooks/analyse.ipynb)

## Vorgehen

1. **Extract:** Zähldaten aus der Excel-Datei der Senatsverwaltung (inkl. Qualitätskennzeichen aus den Zellfarben, per `openpyxl`), Wetter über die Bright-Sky-API, Feiertage über das Modul `holidays`
2. **Transform:** Breit- in Langformat, Zählstellen-Codes vereinheitlicht, Qualität je Stunde gekennzeichnet (`ok`, `rekonstruiert`, `unplausibel`, `keine_daten`, `zeitumstellung`), Wetter auf Ortszeit, doppelte Stunden entfernt
3. **Load:** vier Tabellen in MariaDB (`zaehlstelle`, `zaehlung`, `wetter`, `feiertag`), Kontrolle der Zeilenzahlen
4. **Analyse:** SQL-Abfrage ins Notebook, Diagramme, lineare Regression auf log(Anzahl + 1) mit `statsmodels`, Robustheitsprüfungen

Wichtige Festlegungen: Regenstunde = mindestens 0,1 mm Niederschlag. Der Wetterwert mit Zeitstempel 9:00 gehört zur Zählstunde 8–9 Uhr. Fehlende oder unplausible Werte werden weggelassen, nicht ersetzt.

## Projektstruktur

```
radverkehr-berlin/
├── main.py                 # ETL-Pipeline: Extract, Transform, Load
├── docker-compose.yaml     # MariaDB + phpMyAdmin
├── requirements.txt
├── .env.example            # Vorlage für Datenbank-Zugangsdaten
├── src/
│   ├── extract/            # zaehldaten.py, wetter.py
│   ├── transform/          # zaehldaten.py, wetter.py
│   └── load/               # datenbank.py (Verbindung, Laden, Abfrage)
├── sql/
│   ├── db_schema.sql       # Tabellen anlegen
│   └── pruefung.sql        # Prüf-Abfragen
├── notebooks/
│   └── analyse.ipynb       # Analyse und Ergebnisse
├── data/
│   ├── raw/                # Rohdaten (nicht im Repository)
│   └── processed/          # Zwischenergebnisse als CSV (nicht im Repository)
├── docs/
└── logs/                   # etl.log (nicht im Repository)
```

## Ausführen

Voraussetzungen: Python 3, Docker Desktop. Alle Befehle im Projektordner (PowerShell).

1. **Umgebung einrichten**
   ```
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
2. **Zugangsdaten:** `.env.example` nach `.env` kopieren und ein Passwort bei `DB_PASSWORD` eintragen.
3. **Rohdaten:** „Jahresdatei geprüfter Rohdaten der Radzählstellen“ von der [Seite der Senatsverwaltung](https://www.berlin.de/sen/uvk/verkehr/verkehrsplanung/radverkehr/weitere-radinfrastruktur/zaehlstellen-und-fahrradbarometer/) herunterladen und als `data/raw/gesamtdatei-stundenwerte.xlsx` speichern.
4. **Datenbank starten**
   ```
   docker compose up -d
   ```
   Dann phpMyAdmin unter http://localhost:8081 öffnen (Benutzer `root`, Passwort aus `.env`) und `sql/db_schema.sql` in der Datenbank `radverkehr` ausführen.
5. **ETL ausführen** (lädt auch Wetter und Feiertage, dauert einige Minuten)
   ```
   python main.py
   ```
   Erwartete Zeilenzahlen: `zaehlstelle` 35, `zaehlung` 903.120, `wetter` 26.302, `feiertag` 31 (siehe `logs/etl.log`).
6. **Analyse öffnen**
   ```
   python -m jupyter lab
   ```
   `notebooks/analyse.ipynb` öffnen und alle Zellen ausführen.

## Datenquellen und Lizenzen

- **Radzählstellen:** Senatsverwaltung für Mobilität, Verkehr, Klimaschutz und Umwelt Berlin, „Jahresdatei geprüfter Rohdaten der Radzählstellen“, abgerufen am [DATUM EINTRAGEN]. Lizenz: [Datenlizenz Deutschland – Zero – Version 2.0](https://www.govdata.de/dl-de/zero-2-0). Die Daten wurden für dieses Projekt verändert (umgeformt, gefiltert, summiert).
- **Wetter:** Deutscher Wetterdienst (DWD), Station Berlin-Tempelhof (ID 00433), abgerufen am 20.11.2026 über die [Bright-Sky-API](https://brightsky.dev). Lizenz: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Datenbasis: Deutscher Wetterdienst; die Daten wurden für dieses Projekt verändert (Zeitzone, Spaltennamen, doppelte Stunden entfernt).
- **Feiertage:** Python-Modul [`holidays`](https://pypi.org/project/holidays/), Bundesland Berlin.
