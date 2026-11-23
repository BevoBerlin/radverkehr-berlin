# Wettereinfluss auf den Radverkehr in Berlin

Abschlussprojekt meiner Data Science Weiterbildung. Untersucht wird, wie stark das Wetter den Radverkehr in Berlin beeinflusst und ob Nachtschwärmer anders auf Regen reagieren als Pendler. Dafür werden die stündlichen Werte der Berliner Radzählstellen (2023-2025) mit Wetterdaten der DWD-Station Tempelhof verknüpft.

## Ergebnisse

- Bei Regen sind rund 29 % weniger Räder unterwegs, ab 0,5 mm Niederschlag rund 34 %. Pro Grad wärmer sind es knapp 3 % mehr.
- In Ausgehnächten wirkt Regen genauso stark wie im Berufsverkehr (-33 % gegenüber -30 %). Die Vermutung, dass sich Nachtschwärmer weniger abschrecken lassen, hat sich nicht bestätigt.

Die ausführliche Auswertung steht in [`notebooks/analyse.ipynb`](notebooks/analyse.ipynb).

## Projektstruktur

```
├── main.py               # ETL-Skript, füllt die Datenbank
├── docker-compose.yaml   # MariaDB und phpMyAdmin
├── requirements.txt
├── .env.example          # Vorlage für die Zugangsdaten
├── src/
│   ├── extract/          # Zähldaten (Excel) und Wetter (API) einlesen
│   ├── transform/        # Zähl- und Wetterdaten aufbereiten
│   └── load/             # Datenbankverbindung, Laden, Abfragen
├── sql/
│   ├── db_schema.sql     # Tabellen anlegen
│   └── pruefung.sql      # Prüfabfragen
├── notebooks/
│   └── analyse.ipynb     # Analyse und Ergebnisse
└── data/                 # Rohdaten und Zwischenstände, nicht im Repo
```

## Ausführen

Benötigt werden Python 3 und Docker. Alle Befehle laufen im Projektordner:

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

1. `.env.example` nach `.env` kopieren und ein Passwort eintragen.
2. Die Excel-Datei mit den Zähldaten (siehe unten) als `data/raw/gesamtdatei-stundenwerte.xlsx` speichern.
3. `docker compose up -d` ausführen und in phpMyAdmin (http://localhost:8081) `sql/db_schema.sql` laufen lassen.
4. `python main.py` lädt alle Daten in die Datenbank.
5. `python -m jupyter lab` starten und `notebooks/analyse.ipynb` ausführen.

## Daten

Die Zähldaten stammen aus der "Jahresdatei geprüfter Rohdaten der Radzählstellen" der Senatsverwaltung für Mobilität, Verkehr, Klimaschutz und Umwelt Berlin ([Download](https://www.berlin.de/sen/uvk/verkehr/verkehrsplanung/radverkehr/weitere-radinfrastruktur/zaehlstellen-und-fahrradbarometer/)), heruntergeladen am 12.11.2026. Lizenz: [Datenlizenz Deutschland - Zero - Version 2.0](https://www.govdata.de/dl-de/zero-2-0).

Das stündliche Wetter der Station Berlin-Tempelhof kommt über die [Bright-Sky-API](https://brightsky.dev), abgerufen am 20.11.2026. Datenbasis: Deutscher Wetterdienst, Lizenz: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Beide Datensätze wurden für das Projekt verändert.

Die Feiertage liefert das Python-Paket [`holidays`](https://pypi.org/project/holidays/).
