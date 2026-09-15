from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schema.factura_schema import (
    FacturaCreate,
    FacturaUpdateEstado,
    FacturaOut
)
from app.controllers.factura_controller import (
    crear_factura,
    obtener_facturas,
    obtener_factura_por_id,
    obtener_factura_por_agenda,
    actualizar_estado_factura
)
from app.utils.response import response_success, response_error

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


# =========================================================
# CREAR FACTURA
# =========================================================

@router.post("")
def registrar(datos: FacturaCreate, db: Session = Depends(get_db)):
    try:
        nueva = crear_factura(db, datos.model_dump())
        return response_success(
            mensaje="Factura registrada exitosamente",
            data=FacturaOut.model_validate(nueva).model_dump(),
            code=201
        )
    except ValueError as error:
        return response_error(
            mensaje=str(error),
            error="FACTURA_VALIDATION_ERROR",
            code=400
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al registrar la factura",
            error=str(error),
            code=500
        )


# =========================================================
# LISTAR FACTURAS
# =========================================================

@router.get("")
def listar(db: Session = Depends(get_db)):
    try:
        registros = obtener_facturas(db)
        data = [FacturaOut.model_validate(r).model_dump() for r in registros]
        return response_success(
            mensaje="Lista de facturas obtenida con éxito",
            data=data,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al obtener la lista de facturas",
            error=str(error),
            code=500
        )


# =========================================================
# OBTENER FACTURA POR ID
# =========================================================

@router.get("/{id_factura}")
def obtener_por_id(id_factura: int, db: Session = Depends(get_db)):
    try:
        factura = obtener_factura_por_id(db, id_factura)
        if not factura:
            return response_error(
                mensaje=f"No se encontró la factura con ID {id_factura}",
                error="FACTURA_NOT_FOUND",
                code=404
            )
        return response_success(
            mensaje="Factura encontrada",
            data=FacturaOut.model_validate(factura).model_dump(),
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar la factura",
            error=str(error),
            code=500
        )


# =========================================================
# OBTENER FACTURA DE UNA AGENDA
# =========================================================

@router.get("/agenda/{id_agenda}")
def obtener_por_agenda(id_agenda: int, db: Session = Depends(get_db)):
    try:
        factura = obtener_factura_por_agenda(db, id_agenda)
        if not factura:
            return response_error(
                mensaje=f"La agenda {id_agenda} no tiene factura registrada",
                error="FACTURA_NOT_FOUND",
                code=404
            )
        return response_success(
            mensaje="Factura encontrada",
            data=FacturaOut.model_validate(factura).model_dump(),
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar la factura de la agenda",
            error=str(error),
            code=500
        )


# =========================================================
# ACTUALIZAR ESTADO DE LA FACTURA
# =========================================================

@router.patch("/{id_factura}/estado")
def cambiar_estado(id_factura: int, payload: FacturaUpdateEstado, db: Session = Depends(get_db)):
    try:
        factura = actualizar_estado_factura(db, id_factura, payload.nuevo_estado)
        return response_success(
            mensaje=f"Estado de la factura actualizado a '{factura.estado_factura}'",
            data=FacturaOut.model_validate(factura).model_dump(),
            code=200
        )
    except ValueError as error:
        db.rollback()
        return response_error(
            mensaje=str(error),
            error="FACTURA_UPDATE_FAILED",
            code=400
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al actualizar el estado de la factura",
            error=str(error),
            code=500
        )
