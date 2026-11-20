-- 1. Zählstunden ohne Wetterwert (erwartet 3: Zeitumstellung März)
SELECT COUNT(DISTINCT z.zeitpunkt) AS ohne_wetter
FROM zaehlung z
LEFT JOIN wetter w ON w.zeitpunkt = z.zeitpunkt + INTERVAL 1 HOUR
WHERE w.zeitpunkt IS NULL;

-- 2. Mittel Räder/Stunde, Regen ja/nein (20.11.2026: 98,2 trocken / 62,9 Regen)
SELECT w.niederschlag_mm >= 0.1 AS regen, COUNT(*) AS stunden, ROUND(AVG(z.anzahl), 1) AS mittel 
FROM zaehlung z 
JOIN wetter w ON w.zeitpunkt = z.zeitpunkt + INTERVAL 1 HOUR 
WHERE z.qualitaet = 'ok' 
GROUP BY regen;

-- 3. Werktag 7–9 Uhr, Feiertag ja/nein (186,4 / 16,8)
SELECT f.datum IS NOT NULL AS feiertag, COUNT(*) AS stunden, ROUND(AVG(z.anzahl), 1) AS mittel 
FROM zaehlung z 
LEFT JOIN feiertag f ON f.datum = DATE(z.zeitpunkt) 
WHERE WEEKDAY(z.zeitpunkt) < 5 AND HOUR(z.zeitpunkt) IN (7, 8) AND z.qualitaet = 'ok' 
GROUP BY feiertag;