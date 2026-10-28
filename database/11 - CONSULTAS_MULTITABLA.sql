-- =========================================================
-- CONSULTAS MULTITABLA
-- BASE DE DATOS: CHATBOTBARBER
-- =========================================================

-- 1. VERIFICAR USUARIOS REGISTRADOS
SELECT
    u.id_usuario,
    u.nombres_usuario,
    u.apellidos_usuario,
    u.correo_usuario,
    u.telefono_usuario,
    u.rol_usuario,
    u.fecha_registro_usuario
FROM usuario u
ORDER BY u.id_usuario;

-- 2. VERIFICAR DISPONIBILIDAD DE LOS ESPECIALISTAS
SELECT
    d.id_disponibilidad,
    u.id_usuario AS id_especialista,
    u.nombres_usuario AS nombre_especialista,
    u.apellidos_usuario AS apellidos_especialista,
    u.correo_usuario,
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    d.hora_fin_disponibilidad,
    d.estado_disponibilidad
FROM disponibilidad d
INNER JOIN usuario u ON d.id_especialista = u.id_usuario
ORDER BY
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad;

-- 3. VERIFICAR DISPONIBILIDAD DE UN ESPECIALISTA (Documento real)
SELECT
    d.id_disponibilidad,
    u.id_usuario AS id_especialista,
    u.nombres_usuario AS nombre_especialista,
    u.apellidos_usuario AS apellidos_especialista,
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    d.hora_fin_disponibilidad,
    d.estado_disponibilidad
FROM disponibilidad d
INNER JOIN usuario u ON d.id_especialista = u.id_usuario
WHERE u.id_usuario = '80234567'
ORDER BY
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad;

-- 4. VERIFICAR SERVICIOS Y DISPONIBILIDAD
SELECT
    sd.id_servicio_disponibilidad,
    s.id_servicios,
    s.nombre_servicio,
    s.precio_servicio,
    s.duracion_minutos_servicio,
    u.id_usuario AS id_especialista,
    u.nombres_usuario AS nombre_especialista,
    u.apellidos_usuario AS apellidos_especialista,
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    d.hora_fin_disponibilidad,
    d.estado_disponibilidad
FROM servicio_disponibilidad sd
INNER JOIN servicios s ON sd.id_servicios = s.id_servicios
INNER JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
INNER JOIN usuario u ON d.id_especialista = u.id_usuario
ORDER BY
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    s.nombre_servicio;

-- 5. VERIFICAR AGENDAS CON INFORMACIÓN DEL CLIENTE
SELECT
    a.id_agenda,
    u.id_usuario AS id_cliente,
    u.nombres_usuario AS nombre_cliente,
    u.apellidos_usuario AS apellidos_cliente,
    u.correo_usuario,
    u.telefono_usuario,
    a.estado_agenda,
    a.precio_total,
    a.fecha_creacion_agenda
FROM agenda a
INNER JOIN usuario u ON a.id_cliente = u.id_usuario
ORDER BY
    a.fecha_creacion_agenda DESC;

-- 6. VERIFICAR DETALLE COMPLETO DE LAS CITAS
SELECT
    -- AGENDA
    a.id_agenda,
    a.estado_agenda,
    a.precio_total,
    a.fecha_creacion_agenda,
    -- CLIENTE
    cliente.id_usuario AS id_cliente,
    cliente.nombres_usuario AS nombre_cliente,
    cliente.apellidos_usuario AS apellidos_cliente,
    cliente.correo_usuario AS correo_cliente,
    cliente.telefono_usuario AS telefono_cliente,
    -- SERVICIO
    s.id_servicios,
    s.nombre_servicio,
    s.descripcion_servicio,
    s.precio_servicio,
    s.duracion_minutos_servicio,
    -- DISPONIBILIDAD
    d.id_disponibilidad,
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    d.hora_fin_disponibilidad,
    d.estado_disponibilidad,
    -- ESPECIALISTA
    especialista.id_usuario AS id_especialista,
    especialista.nombres_usuario AS nombre_especialista,
    especialista.apellidos_usuario AS apellidos_especialista,
    especialista.correo_usuario AS correo_especialista,
    especialista.telefono_usuario AS telefono_especialista
FROM agenda a
INNER JOIN usuario cliente ON a.id_cliente = cliente.id_usuario
INNER JOIN detalle dt ON a.id_agenda = dt.id_agenda
INNER JOIN servicio_disponibilidad sd ON dt.id_servicio_disponibilidad = sd.id_servicio_disponibilidad
INNER JOIN servicios s ON sd.id_servicios = s.id_servicios
INNER JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
INNER JOIN usuario especialista ON d.id_especialista = especialista.id_usuario
ORDER BY
    d.fecha_disponibilidad DESC,
    d.hora_inicio_disponibilidad;

-- 7. VERIFICAR FACTURAS COMPLETAS
SELECT
    -- FACTURA
    f.id_factura,
    f.fecha_factura,
    f.subtotal_factura,
    f.iva_factura,
    f.total_factura,
    f.estado_factura,
    f.metodo_pago_factura,
    -- AGENDA
    a.id_agenda,
    a.estado_agenda,
    a.precio_total AS precio_total_agenda,
    -- CLIENTE
    u.id_usuario AS id_cliente,
    u.nombres_usuario AS nombre_cliente,
    u.apellidos_usuario AS apellidos_cliente,
    u.correo_usuario,
    u.telefono_usuario
FROM factura f
INNER JOIN agenda a ON f.id_agenda = a.id_agenda
INNER JOIN usuario u ON a.id_cliente = u.id_usuario
ORDER BY
    f.fecha_factura DESC;

-- 8. CONSULTA COMPLETA GENERAL
SELECT
    -- CLIENTE
    cliente.id_usuario AS id_cliente,
    cliente.nombres_usuario AS nombre_cliente,
    cliente.apellidos_usuario AS apellidos_cliente,
    cliente.correo_usuario AS correo_cliente,
    cliente.telefono_usuario AS telefono_cliente,
    -- AGENDA
    a.id_agenda,
    a.estado_agenda,
    a.precio_total,
    a.fecha_creacion_agenda,
    -- SERVICIO
    s.id_servicios,
    s.nombre_servicio,
    s.descripcion_servicio,
    s.precio_servicio,
    s.duracion_minutos_servicio,
    -- DISPONIBILIDAD
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    d.hora_fin_disponibilidad,
    d.estado_disponibilidad,
    -- ESPECIALISTA
    especialista.id_usuario AS id_especialista,
    especialista.nombres_usuario AS nombre_especialista,
    especialista.apellidos_usuario AS apellidos_especialista,
    -- FACTURA
    f.id_factura,
    f.subtotal_factura,
    f.iva_factura,
    f.total_factura,
    f.estado_factura,
    f.metodo_pago_factura
FROM agenda a
INNER JOIN usuario cliente ON a.id_cliente = cliente.id_usuario
INNER JOIN detalle dt ON a.id_agenda = dt.id_agenda
INNER JOIN servicio_disponibilidad sd ON dt.id_servicio_disponibilidad = sd.id_servicio_disponibilidad
INNER JOIN servicios s ON sd.id_servicios = s.id_servicios
INNER JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
INNER JOIN usuario especialista ON d.id_especialista = especialista.id_usuario
LEFT JOIN factura f ON a.id_agenda = f.id_agenda
ORDER BY
    d.fecha_disponibilidad DESC,
    d.hora_inicio_disponibilidad;

-- 9. VERIFICAR FACTURAS PAGADAS
SELECT
    f.id_factura,
    f.fecha_factura,
    f.total_factura,
    f.metodo_pago_factura,
    u.nombres_usuario AS nombre_cliente,
    u.apellidos_usuario AS apellidos_cliente,
    a.id_agenda
FROM factura f
INNER JOIN agenda a ON f.id_agenda = a.id_agenda
INNER JOIN usuario u ON a.id_cliente = u.id_usuario
WHERE f.estado_factura = 'pagada'
ORDER BY
    f.fecha_factura DESC;

-- 10. CITAS PENDIENTES O CONFIRMADAS
SELECT
    a.id_agenda,
    cliente.nombres_usuario AS nombre_cliente,
    cliente.apellidos_usuario AS apellidos_cliente,
    s.nombre_servicio,
    especialista.nombres_usuario AS nombre_especialista,
    especialista.apellidos_usuario AS apellidos_especialista,
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad,
    d.hora_fin_disponibilidad
FROM agenda a
INNER JOIN usuario cliente ON a.id_cliente = cliente.id_usuario
INNER JOIN detalle dt ON a.id_agenda = dt.id_agenda
INNER JOIN servicio_disponibilidad sd ON dt.id_servicio_disponibilidad = sd.id_servicio_disponibilidad
INNER JOIN servicios s ON sd.id_servicios = s.id_servicios
INNER JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
INNER JOIN usuario especialista ON d.id_especialista = especialista.id_usuario
WHERE a.estado_agenda IN ('pendiente', 'confirmada')
ORDER BY
    d.fecha_disponibilidad,
    d.hora_inicio_disponibilidad;