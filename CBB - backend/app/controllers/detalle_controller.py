from sqlalchemy import text
from sqlalchemy.orm import Session

def crear_detalle(db: Session, datos: dict):
    sql = text("""
        INSERT INTO detalle (
            id_agenda,
            id_servicio_disponibilidad
        ) VALUES (
            :id_agenda,
            :id_servicio_disponibilidad
        )
        RETURNING 
            id_detalle,
            id_agenda,
            id_servicio_disponibilidad
    """)
    resultado = db.execute(sql, datos).first()
    db.commit()
    return dict(resultado._mapping) if resultado else None

def obtener_detalle(db: Session):
    sql = text("""
        SELECT 
            id_detalle,
            id_agenda,
            id_servicio_disponibilidad
        FROM detalle
        ORDER BY id_detalle ASC 
    """)
    resultado = db.execute(sql)
    return [dict(row._mapping) for row in resultado]

def obtener_detalle_por_id(db: Session, id_detalle: int):
    sql = text("""
        SELECT 
            id_detalle,
            id_agenda,
            id_servicio_disponibilidad
        FROM detalle
        WHERE id_detalle = :id_detalle
    """)
    resultado = db.execute(sql, {"id_detalle": id_detalle}).first()
    return dict(resultado._mapping) if resultado else None