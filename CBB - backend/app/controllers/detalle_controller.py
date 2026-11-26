from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.detalle import Detalle


# =========================================================
# CREAR DETALLE DE AGENDA
# =========================================================

def crear_detalle(db: Session, datos: dict):
    nuevo = Detalle(
        id_agenda=datos["id_agenda"],
        id_servicio_disponibilidad=datos["id_servicio_disponibilidad"]
    )
    try:
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Ya existe un detalle para esa agenda y ese servicio_disponibilidad, "
        )


# =========================================================
# LISTAR TODOS LOS DETALLES
# =========================================================

def obtener_detalle(db: Session):
    return db.query(Detalle).order_by(Detalle.id_detalle.asc()).all()


# =========================================================
# OBTENER UN DETALLE POR ID
# =========================================================

def obtener_detalle_por_id(db: Session, id_detalle: int):
    return db.query(Detalle).filter(Detalle.id_detalle == id_detalle).first()
