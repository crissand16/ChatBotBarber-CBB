from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.agenda import Agenda
from app.schema.agenda_schema import AgendaCreate
from app.utils.response import estructurar_agendas

# =====================================================
# CREAR UNA AGENDA
# =====================================================

def crear_agenda( 
    db: Session,
    datos: AgendaCreate):
    try:
    # =====================================================
    # 1. VERIFICAR CLIENTE
    # =====================================================

        usuario = db.execute(
            text("""
                SELECT id_usuario
                FROM usuario
                WHERE id_usuario = :id_usuario
            """),
            { #datos.id_usuario para coincidir con la FK
                "id_usuario": datos.id_cliente
            }
        ).first()

        if not usuario:

            raise ValueError(
                "El usuario no existe"
            )


        # =====================================================
        # 2. VERIFICAR DISPONIBILIDAD
        # =====================================================

    #JOIN con servicio_disponibilidad para verificar desde el id_servicio_disponibilidad
        disponibilidad = db.execute(
            text("""
                SELECT
                    d.id_disponibilidad,
                    d.estado_disponibilidad,
                    s.precio_servicio
                FROM servicio_disponibilidad sd

                INNER JOIN disponibilidad d 
                ON sd.id_disponibilidad =
                    d.id_disponibilidad
                
                INNER JOIN servicios s 
                ON sd.id_servicios = s.id_servicios

                WHERE sd.id_servicio_disponibilidad =
                    :id_sd
                FOR UPDATE
            """),
            {
                "id_sd":
                    datos.id_servicio_disponibilidad
            }
        ).first()

        if not disponibilidad:

            raise ValueError(
                "No se encontró el servicio o disponibilidad especificada"
            )


        if disponibilidad.estado_disponibilidad != "disponible":

            raise ValueError(
                "El horario seleccionada ya no está disponible"
            )


        # =========================================================
        # 3. CREAR AGENDA CON EL PRECIO CALCULADO AUTOMÁTICAMENTE
        # =========================================================
        
        # Se crea el objeto ORM con valores del schema
        estado_agenda_val = getattr(datos, "estado_agenda", None) or "pendiente"
        agenda = Agenda(
            id_cliente=datos.id_cliente,
            precio_total=float(disponibilidad.precio_servicio),
            estado_agenda=estado_agenda_val if getattr(datos, "estado_agenda", None) else "pendiente",
            #getattr se usa para asegurar que si el esquema enviado no incluye estado_agenda
            #el backend no colapse y le asigne el valor 'pendiente' por defecto
            fecha_creacion_agenda=datetime.now()
        )

        # Guarda en la base de datos
        db.add(agenda)
        db.flush() #Genera el id_agenda sin guardarlo en la bd
        # definitivamente y sin todavía hacer el commit

    # =====================================================
    # 4. REGISTRAR EL DETALLE DE LA AGENDA
    # =====================================================
        sql_detalle = text("""
                    INSERT INTO detalle (id_agenda, id_servicio_disponibilidad)
                    VALUES (:id_agenda, :id_servicio_disponibilidad)
                """)
        db.execute(sql_detalle, {
            "id_agenda": agenda.id_agenda,
            "id_servicio_disponibilidad": datos.id_servicio_disponibilidad
        })

    # =====================================================
    # 5. ACTUALIZAR DISPONIBILIDAD A 'OCUPADO'
    # =====================================================
        sql_update_disp = text("""
            UPDATE disponibilidad
            SET estado_disponibilidad = 'ocupado'
            WHERE id_disponibilidad = :id_disponibilidad
        """)
        db.execute(sql_update_disp, {"id_disponibilidad": disponibilidad.id_disponibilidad})
        db.commit() #Se guarda la agenda, el detalle y la actualización del estado_disponibilidad
        db.refresh(agenda)
        return agenda
    
    except Exception as e:
        db.rollback()
        raise e



# =========================================================
# LISTAR CITAS POR ESPECIALISTA
# =========================================================

def obtener_citas_especialista(
    db: Session,
    id_especialista: str
):

    sql = text("""
        SELECT
            -- =============================================
            -- AGENDA
            -- =============================================

            a.id_agenda,
            a.id_cliente,
            a.estado_agenda,
            a.precio_total,
            a.fecha_creacion_agenda,

            -- =============================================
            -- CLIENTE
            -- =============================================

            cli.id_usuario AS id_cliente,
            cli.nombres_usuario AS nombres_cliente,
            cli.apellidos_usuario AS apellidos_cliente,

            -- =============================================
            -- DISPONIBILIDAD Y ESPECIALISTA
            -- =============================================

            disp.id_disponibilidad,
            disp.fecha_disponibilidad,
            disp.hora_inicio_disponibilidad,
            esp.id_usuario AS id_especialista,
            esp.nombres_usuario AS nombres_especialista,
            esp.apellidos_usuario AS apellidos_especialista,

            -- =============================================
            -- SERVICIO
            -- =============================================
            
            s.id_servicios,
            s.nombre_servicio,
            s.precio_servicio

        FROM agenda a

        INNER JOIN detalle det
            ON a.id_agenda =
               det.id_agenda

        INNER JOIN servicio_disponibilidad sd
            ON det.id_servicio_disponibilidad =
               sd.id_servicio_disponibilidad

        INNER JOIN servicios s
            ON sd.id_servicios =
               s.id_servicios

        INNER JOIN disponibilidad disp
            ON sd.id_disponibilidad =
               disp.id_disponibilidad

        INNER JOIN usuario esp 
            ON disp.id_especialista = 
            esp.id_usuario
        
        INNER JOIN usuario cli
            ON a.id_cliente =
               cli.id_usuario
        WHERE disp.id_especialista = :id_especialista

        ORDER BY
            disp.fecha_disponibilidad DESC,
            disp.hora_inicio_disponibilidad DESC
    """)

    resultado = db.execute(
        sql,
        {
            "id_especialista": id_especialista
        }
    )
    return estructurar_agendas(resultado)

# =========================================================
# LISTAR AGENDAS POR CLIENTE
# =========================================================
def obtener_agendas_por_cliente(
    db: Session,
    id_cliente: str
):
    sql = text("""
        SELECT
            -- AGENDA
            a.id_agenda,
            a.id_cliente,
            a.estado_agenda,
            a.precio_total,
            a.fecha_creacion_agenda,

            -- CLIENTE
            cli.nombres_usuario AS nombres_cliente,
            cli.apellidos_usuario AS apellidos_cliente,

            -- DISPONIBILIDAD Y ESPECIALISTA
            disp.id_disponibilidad,
            disp.fecha_disponibilidad,
            disp.hora_inicio_disponibilidad,
            esp.id_usuario AS id_especialista,
            esp.nombres_usuario AS nombres_especialista,
            esp.apellidos_usuario AS apellidos_especialista,

            -- SERVICIO
            s.id_servicios,
            s.nombre_servicio,
            s.precio_servicio

        FROM agenda a
        INNER JOIN detalle det 
            ON a.id_agenda = 
            det.id_agenda

        INNER JOIN servicio_disponibilidad sd 
            ON det.id_servicio_disponibilidad = 
            sd.id_servicio_disponibilidad

        INNER JOIN servicios s 
            ON sd.id_servicios = 
            s.id_servicios

        INNER JOIN disponibilidad disp 
            ON sd.id_disponibilidad = 
            disp.id_disponibilidad

        INNER JOIN usuario esp 
            ON disp.id_especialista = 
            esp.id_usuario

        INNER JOIN usuario cli 
            ON a.id_cliente = 
            cli.id_usuario

        WHERE a.id_cliente = :id_cliente
        ORDER BY
            disp.fecha_disponibilidad DESC,
            disp.hora_inicio_disponibilidad DESC
    """)

    resultado = db.execute(sql, {"id_cliente": id_cliente})
    return estructurar_agendas(resultado)


# =========================================================
# LISTAR AGENDAS POR FECHA
# =========================================================
def obtener_agendas_por_fecha(
    db: Session,
    fecha: str
):
    sql = text("""
        SELECT
            -- AGENDA
            a.id_agenda,
            a.id_cliente,
            a.estado_agenda,
            a.precio_total,
            a.fecha_creacion_agenda,

            -- CLIENTE
            cli.nombres_usuario AS nombres_cliente,
            cli.apellidos_usuario AS apellidos_cliente,

            -- DISPONIBILIDAD Y ESPECIALISTA
            disp.id_disponibilidad,
            disp.fecha_disponibilidad,
            disp.hora_inicio_disponibilidad,
            esp.id_usuario AS id_especialista,
            esp.nombres_usuario AS nombres_especialista,
            esp.apellidos_usuario AS apellidos_especialista,

            -- SERVICIO
            s.id_servicios,
            s.nombre_servicio,
            s.precio_servicio

        FROM agenda a
        INNER JOIN detalle det 
            ON a.id_agenda = 
            det.id_agenda

        INNER JOIN servicio_disponibilidad sd 
            ON det.id_servicio_disponibilidad = 
            sd.id_servicio_disponibilidad

        INNER JOIN servicios s 
            ON sd.id_servicios = 
            s.id_servicios

        INNER JOIN disponibilidad disp 
            ON sd.id_disponibilidad = 
            disp.id_disponibilidad

        INNER JOIN usuario esp 
            ON disp.id_especialista = 
            esp.id_usuario

        INNER JOIN usuario cli 
            ON a.id_cliente = 
            cli.id_usuario

        WHERE disp.fecha_disponibilidad = :fecha
        ORDER BY
            disp.hora_inicio_disponibilidad ASC,
            esp.nombres_usuario ASC
    """)

    resultado = db.execute(sql, {"fecha": fecha})
    return estructurar_agendas(resultado)