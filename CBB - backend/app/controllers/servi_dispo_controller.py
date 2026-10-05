from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.servicio_disponibilidad import ServicioDisponibilidad


# =========================================================
# CREAR SERVICIO - DISPONIBILIDAD
# =========================================================

def crear_servicio_disponibilidad(db: Session, datos: dict):
    nuevo = ServicioDisponibilidad(
        id_servicios=datos["id_servicios"],
        id_disponibilidad=datos["id_disponibilidad"]
    )
    try:
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "El servicio ya está asociado a esa disponibilidad, "
        )


# =========================================================
# LISTAR TODAS LOS SERVICIOS - DISPONIBILIDAD
# =========================================================

def obtener_servicio_disponibilidad(db: Session):
    return (
        db.query(ServicioDisponibilidad)
        .order_by(ServicioDisponibilidad.id_servicio_disponibilidad.asc())
        .all()
    )


# =========================================================
# OBTENER UN SERVICIO - DISPONIBILIDAD POR ID
# =========================================================

def obtener_servicio_disponibilidad_por_id(db: Session, id_servicio_disponibilidad: int):
    return (
        db.query(ServicioDisponibilidad)
        .filter(ServicioDisponibilidad.id_servicio_disponibilidad == id_servicio_disponibilidad)
        .first()
    )
