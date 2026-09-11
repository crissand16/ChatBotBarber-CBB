-- =========================================================
-- INSERTAR USUARIOS DE PRUEBA
-- TOTAL DE USUARIOS 23
-- =========================================================

-- =========================================================
-- 14 CLIENTES
-- =========================================================
INSERT INTO usuario (
    id_usuario, 
    nombres_usuario, 
    apellidos_usuario, 
    tipo_documento_usuario,
    documento_usuario, 
    correo_usuario, 
    contrasena_usuario, 
    fecha_nacimiento_usuario,
    telefono_usuario, 
    rol_usuario,
    fecha_registro_usuario
) 
VALUES
(
    'CL001', 
    'Carlos Alberto', 
    'Gómez Ruiz', 
    'CC', 
    '1018452301', 
    'carlos.gomez@gmail.com', 
    'Carlos2026*', 
    '1995-04-12', 
    '3104567890', 
    'cliente',
    '2026/08/20'
),
(
    'CL002', 
    'Mateo', 
    'Rodríguez Silva', 
    'CC', 
    '1020304050', 
    'mateo.rodriguez@hotmail.com', 
    'Mateo1234*', 
    '1998-08-23', 
    '3112345678', 
    'cliente',
    '2026/07/22'
),
(
    'CL003', 
    'Andrés Felipe', 
    'Martínez Torres', 
    'CC', 
    '1032456789', 
    'andres.martinez@yahoo.com', 
    'Andres2026*', 
    '2001-01-15', 
    '3009876543', 
    'cliente',
    '2026/08/21'
),
(
    'CL004', 
    'Santiago', 
    'López Hernández', 
    'TI', 
    '1098765432', 
    'santiago.lopez@gmail.com', 
    'SantiPass1*', 
    '2007-06-30', 
    '3201239876', 
    'cliente',
    '2026/08/20'
),
(
    'CL005', 
    'Daniel Esteban', 
    'Morales Cruz', 
    'CC', 
    '1015678901', 
    'daniel.morales@outlook.com', 
    'DanielM2026*', 
    '1992-11-05', 
    '3156784321', 
    'cliente',
    '2026/06/19'
),
(
    'CL006', 
    'Alejandro', 
    'Vargas Castro', 
    'PPT', 
    '543210987', 
    'alejo.vargas@gmail.com', 
    'AlejoPass123*', 
    '1996-03-18', 
    '3187654321', 
    'cliente',
    '2026/07/20'
),
(
    'CL007', 
    'Juan José', 
    'Ramírez Gutiérrez', 
    'CC', 
    '1025896314', 
    'juanjo.ramirez@gmail.com', 
    'JuanJo2026*', 
    '2000-09-12', 
    '3014561234', 
    'cliente',
    '2026/08/23'
),
(
    'CL008', 
    'David Ricardo', 
    'Herrera Díaz', 
    'CC', 
    '1019283746', 
    'david.herrera@hotmail.com', 
    'DavidH1234*', 
    '1994-12-01', 
    '3139876543', 
    'cliente',
    '2026/07/23'
),
(
    'CL009', 
    'Gabriel', 
    'Mendoza Sánchez', 
    'TI', 
    '1087654321', 
    'gabriel.mendoza@gmail.com', 
    'GabiPass2026*', 
    '2008-02-28', 
    '3176549870', 
    'cliente',
    '2026/06/16'
),
(
    'CL010', 
    'Nicolás', 
    'Ríos Pineda', 
    'CC',
    '1034567890', 
    'nicolas.rios@outlook.com', 
    'NicoRios123*', 
    '1999-07-22', 
    '3128901234', 
    'cliente',
    '2026/05/20'
),
(
    'CL011', 
    'Samuel', 
    'Castro Medina', 
    'CC', 
    '1012349876', 
    'samuel.castro@gmail.com', 
    'SamuCastro1*', 
    '1997-10-14', 
    '3045678901', 
    'cliente',
    '2026/08/18'
),
(
    'CL012', 
    'Sebastián', 
    'Ortega Marín', 
    'PPT', 
    '654987321', 
    'sebas.ortega@yahoo.com', 
    'Sebas2026*', 
    '1993-05-09', 
    '3162345678', 
    'cliente',
    '2026/07/26'
),
(
    'CL013', 
    'Lucas', 
    'Jiménez Romero', 
    'CC', 
    '1028374651', 
    'lucas.jimenez@gmail.com', 
    'LucasJ1234*', 
    '2002-04-03', 
    '3029876543', 
    'cliente',
    '2026/07/27'
),
(

    'CL014', 
    'Tomas', 
    'Suárez Navarro', 
    'CC',
    '1039485762', 
    'tomas.suarez@outlook.com', 
    'TomasS2026*', 
    '1990-08-19', 
    '3145671234', 
    'cliente',
    '2026/05/20'
);


-- =========================================================
-- 7 ESPECIALISTAS
-- =========================================================
INSERT INTO usuario (
    id_usuario,
    nombre,
    apellidos,
    telefono,
    correo,
    direccion,
    contrasena,
    especializacion,
    tipo,
    rol
)
VALUES
(
    'ES002', 
    'Camilo Andrés', 
    'Rojas Parra', 
    'CC', 
    '80234567', 
    'camilo.rojas@barberia.com', 
    'CamiloBarber1*', 
    '1991-06-20', 
    '3112223344', 
    'especialista',
    '2026/08/20'
),
(
    'ES001', 
    'Javier Eduardo', 
    'Pérez Moreno', 
    'CC', 
    '80123456', 
    'javier.perez@barberia.com', 
    'BarberoJavi1*', 
    '1988-03-15', 
    '3101112233', 
    'especialista',
    '2026/08/21'
),
(
    'ES003', 
    'Diego Fernando', 
    'Bermúdez Gil', 
    'CC', 
    '80345678', 
    'diego.bermudez@barberia.com', 
    'DiegoCut2026*', 
    '1994-01-10', 
    '3123334455', 
    'especialista',
    '2026/08/24'
),
(
    'ES004', 
    'Oscar Ivan', 
    'Salazar Ortiz', 
    'CC', 
    '80456789', 
    'oscar.salazar@barberia.com', 
    'OscarBarber2026*', 
    '1989-11-25', 
    '3134445566', 
    'especialista',
    '2026/08/22'
),
(
    'ES005', 
    'Felipe', 
    'Guerrero Cárdenas', 
    'CC', 
    '80567890', 
    'felipe.guerrero@barberia.com', 
    'FelipeBarber1*', 
    '1993-09-04', 
    '3145556677', 
    'especialista',
    '2026/06/26'
),
(
    'ES006', 
    'Julian David', 
    'Acosta Vela', 
    'CC', 
    '80678901', 
    'julian.acosta@barberia.com', 
    'JulianAcosta1*', 
    '1996-07-17', 
    '3156667788', 
    'especialista',
    '2026/06/20'
),
(
    'ES007', 
    'Leonardo', 
    'Franco Meza', 
    'CC', 
    '80789012', 
    'leonardo.franco@barberia.com', 
    'LeoBarber2026*', 
    '1990-04-22', 
    '3167778899', 
    'especialista'
    '2026/08/27'
);


-- =========================================================
-- 2 ADMINISTRADORES
-- =========================================================
INSERT INTO usuario (
    id_usuario,
    nombre,
    apellidos,
    telefono,
    correo,
    direccion,
    contrasena,
    especializacion,
    tipo,
    rol
)
VALUES
(
    'AD001', 
    'Roberto', 
    'Mora Villalobos', 
    'CC', 
    '79123456', 
    'admin.roberto@barberia.com', 
    'AdminRoberto2026*', 
    '1984-01-20', 
    '3007778899', 
    'admin',
    '2026/07/20'
),
(
    'AD002', 
    'Patricia', 
    'Hurtado Bernal', 
    'CC', 
    '52987654', 
    'admin.patricia@barberia.com', 
    'AdminPatri2026*', 
    '1985-09-14', 
    '3018889900', 
    'admin'
    '2026/06/20'
);