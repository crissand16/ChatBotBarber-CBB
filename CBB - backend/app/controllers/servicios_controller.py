from sqlalchemy import text
from sqlalchemy.orm import Session

def listar_servicios(db: Session):
    sql = text("""
        SELECT 
            id_servicios,
            nombre_servicio,
            precio_servicio,
            duracion_minutos_servicio,
            descripcion_servicio
        FROM servicios
        ORDER BY id_servicios ASC
    """)
    resultado = db.execute(sql)
    return [dict(row._mapping) for row in resultado]

def obtener_servicio_por_id(db: Session, id_servicios: int):
    sql = text("""
        SELECT 
            id_servicios,
            nombre_servicio,
            precio_servicio,
            duracion_minutos_servicio,
            descripcion_servicio
        FROM servicios
        WHERE id_servicios = :id_servicios
    """)
    resultado = db.execute(sql, {"id_servicios": id_servicios}).first()
    return dict(resultado._mapping) if resultado else None

def crear_servicio(db: Session, datos: dict):
    sql = text("""
        INSERT INTO servicios (
            nombre_servicio,
            precio_servicio,
            duracion_minutos_servicio,
            descripcion_servicio
        ) VALUES (
            :nombre_servicio,
            :precio_servicio,
            :duracion_minutos_servicio,
            :descripcion_servicio
        )
        RETURNING 
            id_servicios,
            nombre_servicio,
            precio_servicio,
            duracion_minutos_servicio,
            descripcion_servicio
    """)
    resultado = db.execute(sql, datos).first()
    db.commit()
    return dict(resultado._mapping) if resultado else None