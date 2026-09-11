from sqlalchemy import text
from sqlalchemy.orm import Session

def crear_servicio_disponibilidad(db: Session, datos: dict):
    sql = text("""
        INSERT INTO servicio_disponibilidad (
            id_servicios,
            id_disponibilidad
        ) VALUES (
            :id_servicios,
            :id_disponibilidad
        )
        RETURNING 
            id_servicio_disponibilidad,
            id_servicios,
            id_disponibilidad
    """)
    resultado = db.execute(sql, datos).first()
    db.commit()
    return dict(resultado._mapping) if resultado else None


def obtener_servicio_disponibilidad(db: Session):
    sql = text("""
        SELECT 
            id_servicio_disponibilidad,
            id_servicios,
            id_disponibilidad
        FROM servicio_disponibilidad
        ORDER BY id_servicio_disponibilidad ASC
    """)
    resultado = db.execute(sql)
    #Mapear cada fila a un diccionario de Python
    return [dict(row._mapping) for row in resultado]

def obtener_servicio_disponibilidad_por_id(db: Session):
    sql = text("""
        SELECT 
            id_servicio_disponibilidad,
            id_servicios,
            id_disponibilidad
        FROM servicio_disponibilidad
        WHERE id_servicio_disponibilidad = :id_servicio_disponibilidad
    """)
    resultado = db.execute(sql, {"id_servicio_disponibilidad": id_servicio_disponibilidad}).first()
    return dict(resultado._mapping) if resultado else None