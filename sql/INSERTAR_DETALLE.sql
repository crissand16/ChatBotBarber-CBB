-- =========================================================
-- TABLA DETALLE
-- =========================================================

INSERT INTO detalle (
    id_agenda,
    id_servicio_disponibilidad
)
SELECT
    1,                                   -- ID de la agenda creada
    sd.id_servicio_disponibilidad
FROM servicio_disponibilidad sd
JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
WHERE d.id_especialista = 'ES001'
  AND d.fecha_disponibilidad = DATE '2026-08-24'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00';


INSERT INTO detalle (
    id_agenda,
    id_servicio_disponibilidad
)
SELECT
    2,                                   
    sd.id_servicio_disponibilidad
FROM servicio_disponibilidad sd
JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
WHERE d.id_especialista = 'ES006'
  AND d.fecha_disponibilidad = DATE '2026-08-26'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00';