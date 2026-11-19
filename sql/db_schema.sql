-- Schema für das Projekt "Wettereinfluss auf den Radverkehr in Berlin"


DROP TABLE IF EXISTS zaehlung;
DROP TABLE IF EXISTS zaehlstelle;
DROP TABLE IF EXISTS wetter;
DROP TABLE IF EXISTS feiertag;

CREATE TABLE zaehlstelle (
    zaehlstelle_code  VARCHAR(20)   NOT NULL,
    standort_code     VARCHAR(20)   NOT NULL,
    name              VARCHAR(100)  NOT NULL,
    streckentyp       ENUM('ausgehen', 'pendeln') NULL,
    PRIMARY KEY (zaehlstelle_code)
);

CREATE TABLE zaehlung (
    zaehlstelle_code  VARCHAR(20)        NOT NULL,
    zeitpunkt         DATETIME           NOT NULL,
    anzahl            SMALLINT UNSIGNED  NULL,
    qualitaet         ENUM('ok', 'rekonstruiert', 'unplausibel',
                           'keine_daten', 'zeitumstellung') NOT NULL,
    PRIMARY KEY (zaehlstelle_code, zeitpunkt),
    FOREIGN KEY (zaehlstelle_code) REFERENCES zaehlstelle (zaehlstelle_code)
);

CREATE TABLE wetter (
    zeitpunkt         DATETIME      NOT NULL,
    niederschlag_mm   DECIMAL(4,1)  NULL,
    temperatur_c      DECIMAL(4,1)  NULL,
    wind_kmh          DECIMAL(4,1)  NULL,
    PRIMARY KEY (zeitpunkt)
);

CREATE TABLE feiertag (
    datum             DATE          NOT NULL,
    name              VARCHAR(60)   NOT NULL,
    PRIMARY KEY (datum)
);
