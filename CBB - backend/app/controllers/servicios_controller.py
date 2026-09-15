from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.servicios import Servicios


def listar_servicios(db: Session):
    return (
        db.query(Servicios)
        .order_by(Servicios.id_servicios.asc())
        .all()
    )


def obtener_servicio_por_id(db: Session, id_servicios: int):
    return (
        db.query(Servicios)
        .filter(Servicios.id_servicios == id_servicios)
        .first()
    )


def crear_servicio(db: Session, datos: dict):
    nuevo = Servicios(
        nombre_servicio=datos["nombre_servicio"],
        precio_servicio=datos["precio_servicio"],
        duracion_minutos_servicio=datos["duracion_minutos_servicio"],
        descripcion_servicio=datos.get("descripcion_servicio")
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# =========================================================
# ACTUALIZAR UN SERVICIO (parcial)
# =========================================================

def actualizar_servicio(db: Session, id_servicios: int, datos: dict):
    servicio = (
        db.query(Servicios)
        .filter(Servicios.id_servicios == id_servicios)
        .first()
    )

    if not servicio:
        return None

    campos_actualizables = (
        "nombre_servicio",
        "precio_servicio",
        "duracion_minutos_servicio",
        "descripcion_servicio"
    )

    for campo in campos_actualizables:
        if datos.get(campo) is not None:
            setattr(servicio, campo, datos[campo])

    db.commit()
    db.refresh(servicio)
    return servicio


# =========================================================
# ELIMINAR UN SERVICIO
# =========================================================

def eliminar_servicio(db: Session, id_servicios: int):
    servicio = (
        db.query(Servicios)
        .filter(Servicios.id_servicios == id_servicios)
        .first()
    )

    if not servicio:
        return None

    try:
        db.delete(servicio)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "No se puede eliminar el servicio porque tiene disponibilidad "
            "u órdenes asociadas. Considere desactivarlo en vez de eliminarlo."
        )
