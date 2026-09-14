from sqlalchemy.orm import Session

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
