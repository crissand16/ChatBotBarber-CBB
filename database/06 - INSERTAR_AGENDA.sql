-- =========================================================
-- CREACIÓN DE AGENDA
-- =========================================================

-- CITA 1
INSERT INTO agenda (
    id_cliente,
    estado_agenda,
    precio_total,
    fecha_creacion
)
SELECT
    'CL001',                
    'confirmada',  
    45000.00,                      
    NOW()                               
FROM disponibilidad d
WHERE d.id_especialista = 'ES001'       -- Especialista seleccionado
  AND d.fecha_disponibilidad = DATE '2026-08-25'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00'
  AND d.estado_disponibilidad = 'disponible';

-- CITA 2
INSERT INTO agenda (
    id_cliente,
    estado_agenda,
    precio_total,
    fecha_creacion
)
SELECT
    'CL004',                
    'confirmada',  
    25000.00,                      
    NOW()                               
FROM disponibilidad d
WHERE d.id_especialista = 'ES006'       
  AND d.fecha_disponibilidad = DATE '2026-08-26'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00'
  AND d.estado_disponibilidad = 'disponible';