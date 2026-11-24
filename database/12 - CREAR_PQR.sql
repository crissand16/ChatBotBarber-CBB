-- =========================================================
-- 12. BUZÓN PQR (peticiones, quejas y reclamos)
-- =========================================================
-- Opcional: el backend crea esta tabla automáticamente al arrancar si no
-- existe. Este script sirve para crearla a mano (pgAdmin / psql).

CREATE TABLE IF NOT EXISTS pqr (
    id_pqr              SERIAL PRIMARY KEY,
    id_usuario          VARCHAR(10)  NOT NULL REFERENCES usuario (id_usuario),
    nombre_pqr          VARCHAR(100) NOT NULL,
    correo_pqr          VARCHAR(60)  NOT NULL,
    tipo_pqr            VARCHAR(15)  NOT NULL,
    asunto_pqr          VARCHAR(120) NOT NULL,
    mensaje_pqr         TEXT         NOT NULL,
    estado_pqr          VARCHAR(20)  NOT NULL DEFAULT 'recibida',
    correo_enviado_pqr  BOOLEAN      NOT NULL DEFAULT FALSE,
    fecha_creacion_pqr  TIMESTAMP    NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_pqr_tipo
        CHECK (tipo_pqr IN ('peticion', 'queja', 'reclamo')),
    CONSTRAINT chk_pqr_estado
        CHECK (estado_pqr IN ('recibida', 'en_proceso', 'respondida', 'cerrada'))
);

-- PQR que quedaron guardadas pero cuyo correo no se pudo enviar
-- SELECT * FROM pqr WHERE correo_enviado_pqr = FALSE ORDER BY fecha_creacion_pqr;
