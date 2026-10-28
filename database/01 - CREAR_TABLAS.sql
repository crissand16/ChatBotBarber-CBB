-- ==================================
-- BASE DE DATOS: chatbotbarber
-- SISTEMA DE GESTIÓN DE CITAS DE BARBERÍA
-- MOTOR: PostgreSQL
-- ==================================

-- ==================================
-- TABLA: Usuario
-- ==================================

CREATE TABLE usuario (
    id_usuario VARCHAR(10) PRIMARY KEY,
    nombres_usuario VARCHAR(40) NOT NULL,
    apellidos_usuario VARCHAR(40) NOT NULL,
    tipo_documento_usuario VARCHAR(10) NOT NULL DEFAULT 'CC',
    documento_usuario VARCHAR(10) NOT NULL UNIQUE,
    correo_usuario VARCHAR(60) NOT NULL UNIQUE,
    contrasena_usuario VARCHAR(255) NOT NULL,
    fecha_nacimiento_usuario DATE NOT NULL,
    telefono_usuario VARCHAR(20) NOT NULL,
    rol_usuario VARCHAR(20) NOT NULL DEFAULT 'cliente',
    fecha_registro_usuario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_usuario_tipo_documento
        CHECK (
            tipo_documento_usuario IN (
                'TI',
                'CC',
                'PPT'
            )
        ),
    
    CONSTRAINT chk_usuario_rol
        CHECK (
            rol_usuario IN (
                'cliente',
                'especialista',
                'admin'
            )
        )
);


-- =================================
-- TABLA: Disponibilidad
-- =================================

CREATE TABLE disponibilidad(
    id_disponibilidad SERIAL PRIMARY KEY,
    id_especialista VARCHAR(10) NOT NULL,
    fecha_disponibilidad DATE NOT NULL,
    hora_inicio_disponibilidad TIME NOT NULL,
    hora_fin_disponibilidad TIME NOT NULL,
    estado_disponibilidad VARCHAR(20) DEFAULT 'ocupado',

    CONSTRAINT chk_disponibilidad_estado 
        CHECK (
            estado_disponibilidad IN (
                'disponible',
                'ocupado'
            )
        ),

    CONSTRAINT fk_disponibilidad_especialista
        FOREIGN KEY (id_especialista)
        REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_dispobilidad_especialista_fecha_hora
        UNIQUE (
            id_especialista,
            fecha_disponibilidad,
            hora_inicio_disponibilidad
        )
);

-- ==================================
-- TABLA: Servicios
-- ==================================

CREATE TABLE servicios (
    id_servicios SERIAL PRIMARY KEY,
    nombre_servicio VARCHAR(70) NOT NULL,
    precio_servicio DECIMAL(10,2) NOT NULL 
        CHECK(precio_servicio >= 0),
    duracion_minutos_servicio INTEGER NOT NULL DEFAULT 30
        CHECK(duracion_minutos_servicio > 0),
    descripcion_servicio VARCHAR(200) NULL 
);

-- ==================================
-- TABLA INTERMEDIA: Servicio_Disponibilidad
-- RELACIÓN: servicios - disponibilidad
-- ==================================

CREATE TABLE servicio_disponibilidad (
    id_servicio_disponibilidad SERIAL PRIMARY KEY,
    id_servicios INTEGER NOT NULL,
    id_disponibilidad INTEGER NOT NULL,

-- Restricción 1: Relación con la tabla servicio
    CONSTRAINT fk_servicio_disponibilidad_servicio
        FOREIGN KEY (id_servicios)
        REFERENCES servicios(id_servicios)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

-- Restricción 2: Relación con la tabla disponibilidad
    CONSTRAINT fk_servicio_disponibilidad_disponibilidad
        FOREIGN KEY (id_disponibilidad)
        REFERENCES disponibilidad(id_disponibilidad)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
-- Restricción 3: Evitar asociar el mismo servicio a la misma disponibilidad más de una vez
    CONSTRAINT uq_servicio_disponibilidad
        UNIQUE (
            id_servicios,
            id_disponibilidad
        )
);

-- ==================================
-- TABLA Agenda
-- ==================================

CREATE TABLE agenda (
    id_agenda SERIAL PRIMARY KEY,
    id_cliente VARCHAR(10) NOT NULL,
    estado_agenda VARCHAR(20) NOT NULL,
    precio_total DECIMAL(10,2) NOT NULL
        CHECK (precio_total >= 0),
    fecha_creacion_agenda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_agenda_estado
        CHECK (
            estado_agenda IN (
                'pendiente',
                'completada'
            )
        ),

    CONSTRAINT fk_agenda_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES usuario(id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ==================================
-- TABLA Detalle
-- ==================================

CREATE TABLE detalle (
    id_detalle SERIAL PRIMARY KEY,
    id_agenda INTEGER NOT NULL,
    id_servicio_disponibilidad INTEGER NOT NULL,

-- Restricción 1: Relación con la tabla agenda
    CONSTRAINT fk_detalle_agenda 
        FOREIGN KEY (id_agenda)
        REFERENCES agenda(id_agenda)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

-- Restricción 2: Relación con la tabla servicio_disponibilidad
    CONSTRAINT fk_detalle_disponibilidad_servicio
        FOREIGN KEY (id_servicio_disponibilidad)
        REFERENCES servicio_disponibilidad(id_servicio_disponibilidad)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

-- Restricción 3: Evitar asociar la misma agenda al mismo servicio_disponibilidad más de una vez
    CONSTRAINT uq_detalle
        UNIQUE (
            id_agenda,
            id_servicio_disponibilidad
        )
);

-- ==================================
-- TABLA Factura
-- ==================================

CREATE TABLE Factura (
    id_factura SERIAL PRIMARY KEY,
    fecha_factura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal_factura DECIMAL(10,2) NOT NULL
        CHECK(subtotal_factura >= 0),
    iva_factura DECIMAL(10,2) NOT NULL  
        CHECK(iva_factura >= 0),
    total_factura DECIMAL(10,2) NOT NULL
        CHECK(total_factura >= 0),
    estado_factura VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    metodo_pago_factura VARCHAR(20) NOT NULL DEFAULT 'efectivo',
    id_agenda INTEGER NOT NULL UNIQUE,

    CONSTRAINT fk_factura_agenda
        FOREIGN KEY (id_agenda)
        REFERENCES Agenda(id_agenda)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_factura_estado
        CHECK (
            estado_factura IN (
                    'pendiente',
                    'pagada'
            )
        ),
    
    CONSTRAINT chk_factura_metodo_pago
        CHECK(
            metodo_pago_factura IN (
                    'efectivo',
                    'transferencia'
            )
        )
);

-- =========================================================
-- FIN DEL SCRIPT
-- =========================================================