CREATE OR REPLACE VIEW avg_temp_por_ambiente AS
SELECT
    room_id,
    ROUND(AVG(temp)::numeric, 2) AS avg_temp
FROM temperature_readings
GROUP BY room_id;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    reading_hour AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
GROUP BY reading_hour
ORDER BY reading_hour;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    reading_date AS data,
    MAX(temp) AS temp_max,
    MIN(temp) AS temp_min
FROM temperature_readings
GROUP BY reading_date
ORDER BY reading_date;

CREATE OR REPLACE VIEW media_temp_in_out AS
SELECT
    location_type,
    ROUND(AVG(temp)::numeric, 2) AS avg_temp
FROM temperature_readings
GROUP BY location_type;
