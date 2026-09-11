from sqlalchemy import text
from sqlalchemy.orm import Session


# =========================================================
# OBTENER TODA LA DISPONIBILIDAD DE UN ESPECIALISTA
# =========================================================

def obtener_disponibilidad_especialista(
    db: Session,
    id_especialista: str
):
    sql = text("""
        SELECT
            d.id_disponibilidad,
            d.id_especialista,
            u.nombres_usuario,
            u.apellidos_usuario,
            d.fecha_disponibilidad,
            d.hora_inicio_disponibilidad,
            d.hora_fin_disponibilidad,
            d.estado_disponibilidad
        FROM disponibilidad d
        INNER JOIN usuario u
            ON d.id_especialista = u.id_usuario
        WHERE d.id_especialista = :id_especialista
        ORDER BY
            d.fecha_disponibilidad,
            d.hora_inicio_disponibilidad
    """)

    resultado = db.execute(
        sql,
        {
            "id_especialista": id_especialista
        }
    )

    return [
        dict(row._mapping)
        for row in resultado
    ]


# =========================================================
# OBTENER DISPONIBILIDAD DE TODOS LOS ESPECIALISTAS
# ENTRE DOS FECHAS
# =========================================================

def obtener_disponibilidad_rango(
    db: Session,
    fecha_inicio,
    fecha_fin
):
    sql = text("""
        SELECT
            d.id_disponibilidad,
            d.id_especialista,
            u.nombres_usuario,
            u.apellidos_usuario,
            d.fecha_disponibilidad,
            d.hora_inicio_disponibilidad,
            d.hora_fin_disponibilidad,
            d.estado_disponibilidad
        FROM disponibilidad d
        INNER JOIN usuario u
            ON d.id_especialista = u.id_usuario
        WHERE u.rol_usuario = 'especialista'
          AND d.fecha_disponibilidad BETWEEN :fecha_inicio AND :fecha_fin
        ORDER BY
            d.fecha_disponibilidad,
            u.nombres_usuario,
            u.apellidos_usuario,
            d.hora_inicio_disponibilidad
    """)

    resultado = db.execute(
        sql,
        {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
    )

    return [
        dict(row._mapping)
        for row in resultado
    ]
