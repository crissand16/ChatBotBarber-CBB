-- ==================================
-- BASE DE DATOS: chatbotbarber
-- SISTEMA DE GESTIÓN DE CITAS DE BARBERÍA
-- MOTOR: PostgreSQL
-- TRIGGER O DISPARADORES AUTOMATICOS
-- ==================================



-- =========================================================
-- TRIGGER 1
-- VALIDAR QUE EL USUARIO DE LA DISPONIBILIDAD
-- SEA REALMENTE UN ESPECIALISTA
-- =========================================================

CREATE OR REPLACE FUNCTION validar_especialista()
RETURNS TRIGGER AS $$
BEGIN

    IF NOT EXISTS (

        SELECT 1
        FROM usuario
        WHERE id_usuario = NEW.id_especialista
        AND rol_usuario = 'especialista'

    ) THEN

        RAISE EXCEPTION
        'El usuario % no tiene el rol de especialista',
        NEW.id_especialista;

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validar_especialista

BEFORE INSERT OR UPDATE
ON disponibilidad

FOR EACH ROW

EXECUTE FUNCTION validar_especialista();


-- =========================================================
-- TRIGGER 2
-- VALIDAR QUE EL USUARIO DE LA AGENDA
-- SEA REALMENTE UN CLIENTE
-- =========================================================

CREATE OR REPLACE FUNCTION validar_cliente()
RETURNS TRIGGER AS $$
BEGIN

    IF NOT EXISTS (

        SELECT 1
        FROM usuario
        WHERE id_usuario = NEW.id_cliente
        AND rol_usuario = 'cliente'

    ) THEN

        RAISE EXCEPTION
        'El usuario % no tiene el rol de cliente',
        NEW.id_cliente;

    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validar_cliente

BEFORE INSERT OR UPDATE
ON agenda

FOR EACH ROW

EXECUTE FUNCTION validar_cliente();


-- =========================================================
-- TRIGGER 3
-- VALIDAR QUE LA DISPONIBILIDAD
-- NO ESTÉ OCUPADA ANTES DE RESERVAR
-- =========================================================

CREATE OR REPLACE FUNCTION validar_disponibilidad()
RETURNS TRIGGER AS $$

DECLARE

    estado_actual VARCHAR(20);

BEGIN

    SELECT d.estado_disponibilidad

    INTO estado_actual

    FROM servicio_disponibilidad sd

    INNER JOIN disponibilidad d

        ON sd.id_disponibilidad =
           d.id_disponibilidad

    WHERE sd.id_servicio_disponibilidad =
          NEW.id_servicio_disponibilidad;


    IF estado_actual = 'ocupado' THEN

        RAISE EXCEPTION
        'Esta disponibilidad ya se encuentra ocupada';

    END IF;


    RETURN NEW;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validar_disponibilidad

BEFORE INSERT
ON detalle

FOR EACH ROW

EXECUTE FUNCTION validar_disponibilidad();


-- =========================================================
-- TRIGGER 4
-- OCUPAR AUTOMÁTICAMENTE LA DISPONIBILIDAD
-- CUANDO SE REALIZA UNA RESERVA
-- =========================================================

CREATE OR REPLACE FUNCTION ocupar_disponibilidad()

RETURNS TRIGGER AS $$

DECLARE

    disponibilidad_id INTEGER;

BEGIN

    SELECT id_disponibilidad

    INTO disponibilidad_id

    FROM servicio_disponibilidad

    WHERE id_servicio_disponibilidad =
          NEW.id_servicio_disponibilidad;


    UPDATE disponibilidad

    SET estado_disponibilidad = 'ocupado'

    WHERE id_disponibilidad =
          disponibilidad_id;


    RETURN NEW;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_ocupar_disponibilidad

AFTER INSERT
ON detalle

FOR EACH ROW

EXECUTE FUNCTION ocupar_disponibilidad();


-- =========================================================
-- TRIGGER 5
-- ACTUALIZAR AUTOMÁTICAMENTE
-- EL PRECIO TOTAL DE LA AGENDA
-- =========================================================

CREATE OR REPLACE FUNCTION actualizar_precio_total_agenda()

RETURNS TRIGGER AS $$

DECLARE

    agenda_afectada INTEGER;

BEGIN

    IF TG_OP = 'DELETE' THEN

        agenda_afectada := OLD.id_agenda;

    ELSE

        agenda_afectada := NEW.id_agenda;

    END IF;


    UPDATE agenda

    SET precio_total = COALESCE(

        (

            SELECT SUM(s.precio_servicio)

            FROM detalle dt

            INNER JOIN servicio_disponibilidad sd

                ON dt.id_servicio_disponibilidad =
                   sd.id_servicio_disponibilidad

            INNER JOIN servicios s

                ON sd.id_servicios =
                   s.id_servicios

            WHERE dt.id_agenda =
                  agenda_afectada

        ),

        0

    )

    WHERE id_agenda =
          agenda_afectada;


    RETURN NULL;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_actualizar_precio_agenda

AFTER INSERT OR DELETE
ON detalle

FOR EACH ROW

EXECUTE FUNCTION actualizar_precio_total_agenda();


-- =========================================================
-- TRIGGER 6
-- LIBERAR LA DISPONIBILIDAD SI SE ELIMINA
-- UNA RESERVA DEL DETALLE
-- =========================================================

CREATE OR REPLACE FUNCTION liberar_disponibilidad()

RETURNS TRIGGER AS $$

DECLARE

    disponibilidad_id INTEGER;

BEGIN

    SELECT id_disponibilidad

    INTO disponibilidad_id

    FROM servicio_disponibilidad

    WHERE id_servicio_disponibilidad =
          OLD.id_servicio_disponibilidad;


    UPDATE disponibilidad

    SET estado_disponibilidad = 'disponible'

    WHERE id_disponibilidad =
          disponibilidad_id;


    RETURN OLD;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_liberar_disponibilidad

AFTER DELETE
ON detalle

FOR EACH ROW

EXECUTE FUNCTION liberar_disponibilidad();


-- =========================================================
-- TRIGGER 7
-- VALIDAR QUE UNA FACTURA SOLO PUEDA SER CREADA
-- CUANDO LA AGENDA ESTÉ COMPLETADA
-- =========================================================

CREATE OR REPLACE FUNCTION validar_agenda_completada()

RETURNS TRIGGER AS $$

DECLARE

    estado_actual VARCHAR(20);

BEGIN

    SELECT estado_agenda

    INTO estado_actual

    FROM agenda

    WHERE id_agenda =
          NEW.id_agenda;


    IF estado_actual <> 'completada' THEN

        RAISE EXCEPTION
        'No se puede generar una factura porque la agenda % no está completada',
        NEW.id_agenda;

    END IF;


    RETURN NEW;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_validar_agenda_factura

BEFORE INSERT
ON factura

FOR EACH ROW

EXECUTE FUNCTION validar_agenda_completada();


-- =========================================================
-- TRIGGER 8
-- CALCULAR AUTOMÁTICAMENTE
-- SUBTOTAL, IVA Y TOTAL DE LA FACTURA
-- =========================================================

CREATE OR REPLACE FUNCTION calcular_total_factura()

RETURNS TRIGGER AS $$

DECLARE

    total_agenda DECIMAL(10,2);

BEGIN

    SELECT precio_total

    INTO total_agenda

    FROM agenda

    WHERE id_agenda =
          NEW.id_agenda;


    NEW.subtotal_factura := total_agenda;


    NEW.iva_factura := ROUND(
        total_agenda * 0.19,
        2
    );


    NEW.total_factura :=

        NEW.subtotal_factura
        +
        NEW.iva_factura;


    RETURN NEW;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_calcular_total_factura

BEFORE INSERT OR UPDATE
ON factura

FOR EACH ROW

EXECUTE FUNCTION calcular_total_factura();


-- =========================================================
-- FIN DEL SCRIPT
-- =========================================================