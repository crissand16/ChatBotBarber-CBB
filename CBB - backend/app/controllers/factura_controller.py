from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.factura import Factura
from app.models.agenda import Agenda


# =========================================================
# CREAR FACTURA A PARTIR DE UNA AGENDA
# =========================================================

def crear_factura(db: Session, datos: dict):
    agenda = db.query(Agenda).filter(Agenda.id_agenda == datos["id_agenda"]).first()
    if not agenda:
        raise ValueError("La agenda indicada no existe")

    nueva = Factura(
        id_agenda=datos["id_agenda"],
        subtotal_factura=datos["subtotal_factura"],
        iva_factura=datos["iva_factura"],
        total_factura=datos["total_factura"],
        metodo_pago_factura=datos.get("metodo_pago_factura") or "efectivo"
    )

    try:
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        raise ValueError("La agenda indicada ya tiene una factura registrada")


# =========================================================
# LISTAR TODAS LAS FACTURAS
# =========================================================

def obtener_facturas(db: Session):
    return db.query(Factura).order_by(Factura.id_factura.asc()).all()


# =========================================================
# OBTENER UNA FACTURA POR ID
# =========================================================

def obtener_factura_por_id(db: Session, id_factura: int):
    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


# =========================================================
# OBTENER LA FACTURA DE UNA AGENDA
# =========================================================

def obtener_factura_por_agenda(db: Session, id_agenda: int):
    return db.query(Factura).filter(Factura.id_agenda == id_agenda).first()


# =========================================================
# ACTUALIZAR ESTADO DE UNA FACTURA (pendiente -> pagada)
# =========================================================

def actualizar_estado_factura(db: Session, id_factura: int, nuevo_estado: str):
    factura = obtener_factura_por_id(db, id_factura)
    if not factura:
        raise ValueError("La factura indicada no existe")

    nuevo_estado = nuevo_estado.lower().strip()
    if nuevo_estado not in ("pendiente", "pagada"):
        raise ValueError("Estado no permitido. Use 'pendiente' o 'pagada'")

    factura.estado_factura = nuevo_estado
    db.commit()
    db.refresh(factura)
    return factura
