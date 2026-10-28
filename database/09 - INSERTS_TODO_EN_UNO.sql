-- =========================================================
-- 0. INSERCIÓN DE SERVICIOS (REQUISITO QUE FALTABA)
-- =========================================================
INSERT INTO servicios (
    id_servicios,
    nombre_servicio,
    descripcion_servicio,
    precio_servicio,
    duracion_minutos_servicio
) VALUES
  (1, 'Combo Básico', 'Corte de cabello sencillo', 20000.00, 30),
  (2, 'Combo Barbero', 'Corte de cabello y barba', 45000.00, 45),
  (3, 'Combo Premium', 'Corte, barba y mascarilla facial', 60000.00, 60),
  (4, 'Combo VIP', 'Corte, barba, mascarilla y bebida', 80000.00, 90),
  (5, 'Combo Padre e Hijo', 'Dos cortes sencillos', 35000.00, 60),
  (6, 'Combo Express', 'Arreglo rápido de barba y bordes', 15000.00, 20)
ON CONFLICT (id_servicios) DO NOTHING;


-- =========================================================
-- 1. INSERTAR USUARIOS DE PRUEBA (23 USUARIOS)
-- =========================================================

-- 14 CLIENTES
INSERT INTO usuario (
    id_usuario, 
    nombres_usuario, 
    apellidos_usuario, 
    correo_usuario, 
    contrasena_usuario, 
    fecha_nacimiento_usuario,
    telefono_usuario, 
    rol_usuario,
    fecha_registro_usuario
) 
VALUES
('1018452301', 'Carlos Alberto', 'Gómez Ruiz', 'carlos.gomez@gmail.com', 'Carlos2026*', '1995-04-12', '3104567890', 'cliente', '2026/08/20'),
('1020304050', 'Mateo', 'Rodríguez Silva', 'mateo.rodriguez@hotmail.com', 'Mateo1234*', '1998-08-23', '3112345678', 'cliente', '2026/07/22'),
('1032456789', 'Andrés Felipe', 'Martínez Torres', 'andres.martinez@yahoo.com', 'Andres2026*', '2001-01-15', '3009876543', 'cliente', '2026/08/21'),
('1098765432', 'Santiago', 'López Hernández', 'santiago.lopez@gmail.com', 'SantiPass1*', '2007-06-30', '3201239876', 'cliente', '2026/08/20'),
('1015678901', 'Daniel Esteban', 'Morales Cruz', 'daniel.morales@outlook.com', 'DanielM2026*', '1992-11-05', '3156784321', 'cliente', '2026/06/19'),
('543210987', 'Alejandro', 'Vargas Castro', 'alejo.vargas@gmail.com', 'AlejoPass123*', '1996-03-18', '3187654321', 'cliente', '2026/07/20'),
('1025896314', 'Juan José', 'Ramírez Gutiérrez', 'juanjo.ramirez@gmail.com', 'JuanJo2026*', '2000-09-12', '3014561234', 'cliente', '2026/08/23'),
('1019283746', 'David Ricardo', 'Herrera Díaz', 'david.herrera@hotmail.com', 'DavidH1234*', '1994-12-01', '3139876543', 'cliente', '2026/07/23'),
('1087654321', 'Gabriel', 'Mendoza Sánchez', 'gabriel.mendoza@gmail.com', 'GabiPass2026*', '2008-02-28', '3176549870', 'cliente', '2026/06/16'),
('1034567890', 'Nicolás', 'Ríos Pineda', 'nicolas.rios@outlook.com', 'NicoRios123*', '1999-07-22', '3128901234', 'cliente', '2026/05/20'),
('1012349876', 'Samuel', 'Castro Medina', 'samuel.castro@gmail.com', 'SamuCastro1*', '1997-10-14', '3045678901', 'cliente', '2026/08/18'),
('654987321', 'Sebastián', 'Ortega Marín', 'sebas.ortega@yahoo.com', 'Sebas2026*', '1993-05-09', '3162345678', 'cliente', '2026/07/26'),
('1028374651', 'Lucas', 'Jiménez Romero', 'lucas.jimenez@gmail.com', 'LucasJ1234*', '2002-04-03', '3029876543', 'cliente', '2026/07/27'),
('1039485762', 'Tomas', 'Suárez Navarro', 'tomas.suarez@outlook.com', 'TomasS2026*', '1990-08-19', '3145671234', 'cliente', '2026/05/20')
ON CONFLICT (id_usuario) DO NOTHING;

-- 7 ESPECIALISTAS
INSERT INTO usuario (
    id_usuario, 
    nombres_usuario, 
    apellidos_usuario, 
    correo_usuario, 
    contrasena_usuario, 
    fecha_nacimiento_usuario,
    telefono_usuario, 
    rol_usuario,
    fecha_registro_usuario
)
VALUES
('80234567', 'Camilo Andrés', 'Rojas Parra', 'camilo.rojas@barberia.com', 'CamiloBarber1*', '1991-06-20', '3112223344', 'especialista', '2026/08/20'),
('80123456', 'Javier Eduardo', 'Pérez Moreno', 'javier.perez@barberia.com', 'BarberoJavi1*', '1988-03-15', '3101112233', 'especialista', '2026/08/21'),
('80345678', 'Diego Fernando', 'Bermúdez Gil', 'diego.bermudez@barberia.com', 'DiegoCut2026*', '1994-01-10', '3123334455', 'especialista', '2026/08/24'),
('80456789', 'Oscar Ivan', 'Salazar Ortiz', 'oscar.salazar@barberia.com', 'OscarBarber2026*', '1989-11-25', '3134445566', 'especialista', '2026/08/22'),
('80567890', 'Felipe', 'Guerrero Cárdenas', 'felipe.guerrero@barberia.com', 'FelipeBarber1*', '1993-09-04', '3145556677', 'especialista', '2026/06/26'),
('80678901', 'Julian David', 'Acosta Vela', 'julian.acosta@barberia.com', 'JulianAcosta1*', '1996-07-17', '3156667788', 'especialista', '2026/06/20'),
('80789012', 'Leonardo', 'Franco Meza', 'leonardo.franco@barberia.com', 'LeoBarber2026*', '1990-04-22', '3167778899', 'especialista', '2026/08/27')
ON CONFLICT (id_usuario) DO NOTHING;

-- 2 ADMINISTRADORES
INSERT INTO usuario (
    id_usuario, 
    nombres_usuario, 
    apellidos_usuario, 
    correo_usuario, 
    contrasena_usuario, 
    fecha_nacimiento_usuario,
    telefono_usuario, 
    rol_usuario,
    fecha_registro_usuario
)
VALUES
('79123456', 'Roberto', 'Mora Villalobos', 'admin.roberto@barberia.com', 'AdminRoberto2026*', '1984-01-20', '3007778899', 'admin', '2026/07/20'),
('52987654', 'Patricia', 'Hurtado Bernal', 'admin.patricia@barberia.com', 'AdminPatri2026*', '1985-09-14', '3018889900', 'admin', '2026/06/20')
ON CONFLICT (id_usuario) DO NOTHING;


-- =========================================================
-- 2. DISPONIBILIDAD DE ESPECIALISTAS
-- =========================================================
INSERT INTO disponibilidad (
    id_especialista, 
    fecha_disponibilidad, 
    hora_inicio_disponibilidad, 
    hora_fin_disponibilidad, 
    estado_disponibilidad
)
SELECT
    '80234567',
    fecha_hora::DATE,
    fecha_hora::TIME,
    (fecha_hora + INTERVAL '1 hour')::TIME,
    'disponible'
FROM generate_series(
    TIMESTAMP '2026-08-25 08:00:00',
    TIMESTAMP '2026-08-27 17:00:00',
    INTERVAL '1 hour'
) AS fecha_hora
WHERE fecha_hora::TIME BETWEEN TIME '08:00:00' AND TIME '17:00:00'
ON CONFLICT ON CONSTRAINT uq_dispobilidad_especialista_fecha_hora DO NOTHING;

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
    VALUES 
        ('80123456'), ('80345678'), ('80456789'), ('80567890'), 
        ('80678901'), ('80789012')
) AS esp(id_especialista)
CROSS JOIN generate_series(
    TIMESTAMP '2026-08-24 08:00:00',
    TIMESTAMP '2026-08-28 16:00:00',
    INTERVAL '1 hour'
) AS bloque
WHERE bloque::TIME BETWEEN TIME '08:00:00' AND TIME '16:00:00'
ON CONFLICT ON CONSTRAINT uq_dispobilidad_especialista_fecha_hora DO NOTHING;


-- =========================================================
-- 3. TABLA INTERMEDIA: servicio_disponibilidad
-- =========================================================
INSERT INTO servicio_disponibilidad (id_servicios, id_disponibilidad) VALUES
(2, 1),
(3, 2),
(1, 3),
(4, 4),
(2, 46),
(5, 47),
(1, 48),
(3, 91),
(6, 92),
(2, 93)
ON CONFLICT DO NOTHING;


-- =========================================================
-- 4. CREACIÓN DE AGENDA
-- =========================================================

-- CITA 1
INSERT INTO agenda (
    id_cliente,
    estado_agenda,
    precio_total,
    fecha_creacion_agenda
)
SELECT
    '1018452301',                
    'completada',  
    45000.00,                      
    NOW()                               
FROM disponibilidad d
WHERE d.id_especialista = '80234567'       
  AND d.fecha_disponibilidad = DATE '2026-08-25'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00'
  AND d.estado_disponibilidad = 'disponible';

-- CITA 2
INSERT INTO agenda (
    id_cliente,
    estado_agenda,
    precio_total,
    fecha_creacion_agenda
)
SELECT
    '1098765432',                
    'completada',  
    25000.00,                      
    NOW()                               
FROM disponibilidad d
WHERE d.id_especialista = '80678901'       
  AND d.fecha_disponibilidad = DATE '2026-08-26'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00'
  AND d.estado_disponibilidad = 'disponible';


-- =========================================================
-- 5. TABLA DETALLE (CORREGIDO DOCUMENTOS DE ESPECIALISTAS Y FECHAS)
-- =========================================================
INSERT INTO detalle (
    id_agenda,
    id_servicio_disponibilidad
)
SELECT
    1,
    sd.id_servicio_disponibilidad
FROM servicio_disponibilidad sd
JOIN disponibilidad d ON sd.id_disponibilidad = d.id_disponibilidad
WHERE d.id_especialista = '80234567'
  AND d.fecha_disponibilidad = DATE '2026-08-25'
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
WHERE d.id_especialista = '80678901'
  AND d.fecha_disponibilidad = DATE '2026-08-26'
  AND d.hora_inicio_disponibilidad = TIME '08:00:00';


-- =========================================================
-- 6. TABLA FACTURA (CORREGIDO ID DE AGENDA REALES: 1 Y 2)
-- =========================================================
INSERT INTO factura (
    id_agenda,
    fecha_factura,
    subtotal_factura,
    iva_factura,
    total_factura,
    estado_factura,
    metodo_pago_factura
) VALUES 
(
    1,
    NOW(),
    45000.00,
    8550.00,
    53550.00,
    'pagada',
    'efectivo'
),
(
    2,
    NOW(),
    25000.00,
    4750.00,
    29750.00,
    'pagada',
    'transferencia'
);

