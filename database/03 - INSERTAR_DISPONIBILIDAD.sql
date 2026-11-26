-- =========================================================
-- AGENDA ESPECIALISTA ES001
-- 25, 26 Y 27 DE AGOSTO DE 2026
-- HORARIO: 08:00 A 17:00
-- =========================================================

INSERT INTO disponibilidad (
    id_especialista,
    fecha_disponibilidad,
    hora_inicio_disponibilidad,
    hora_fin_disponibilidad,
    estado_disponibilidad
)
SELECT
    'ES001',
    fecha_hora::DATE,
    fecha_hora::TIME,
    (fecha_hora + INTERVAL '1 hour')::TIME,
    'disponible'
FROM generate_series(
    TIMESTAMP '2026-08-25 08:00:00',
    TIMESTAMP '2026-08-27 17:00:00',
    INTERVAL '1 hour'
) AS fecha_hora
WHERE fecha_hora::TIME BETWEEN TIME '08:00:00' AND TIME '17:00:00';

INSERT INTO disponibilidad (
    id_especialista,
    fecha_disponibilidad,
    hora_inicio_disponibilidad,
    hora_fin_disponibilidad,
    estado_disponibilidad
)
SELECT 
    esp.id_especialista,
    bloque::DATE AS fecha_disponibilidad,
    bloque::TIME AS hora_inicio_disponibilidad,
    (bloque + INTERVAL '1 hour')::TIME AS hora_fin_disponibilidad,
    'disponible' AS estado_disponibilidad
FROM (
    -- Lista de los 14 especialistas
    VALUES 
        ('ES001'), ('ES002'), ('ES003'), ('ES004'), ('ES005'), 
        ('ES006'), ('ES007')
) AS esp(id_especialista)
CROSS JOIN generate_series( --combinará todos los especialistas de la lista con cada una de las horas producidas 
    TIMESTAMP '2026-08-24 08:00:00',
    TIMESTAMP '2026-08-28 16:00:00',
    INTERVAL '1 hour'
) AS bloque --Nombra a cada resultado de fecha y hora producido en la serie como bloque
WHERE bloque::TIME BETWEEN TIME '08:00:00' AND TIME '16:00:00';