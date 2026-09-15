from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schema.detalle_schema import DetalleCreate, DetalleOut
from app.controllers.detalle_controller import (
    crear_detalle,
    obtener_detalle,
    obtener_detalle_por_id
)
from app.utils.response import response_success, response_error

router = APIRouter(
    prefix="/detalle",
    tags=["Detalle"]
)

@router.post("")
def registrar(datos: DetalleCreate, db: Session = Depends(get_db)):
    try:
        nuevo = crear_detalle(db, datos.model_dump())
        return response_success(
            mensaje="Detalle registrado exitosamente",
            data=DetalleOut.model_validate(nuevo).model_dump(),
            code=201
        )
    except ValueError as error:
        return response_error(
            mensaje=str(error),
            error="DETALLE_CREATE_FAILED",
            code=400
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al registrar el detalle",
            error=str(error),
            code=500
        )

@router.get("")
def listar_detalles(db: Session = Depends(get_db)):
    try:
        registros = obtener_detalle(db)
        data = [DetalleOut.model_validate(r).model_dump() for r in registros]
        return response_success(
            mensaje="Lista de detalles obtenida con éxito",
            data=data,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al obtener la lista de detalles",
            error=str(error),
            code=500
        ) 

@router.get("/{id_detalle}")
def obtener_por_id(id_detalle: int, db: Session = Depends(get_db)):
    try:
        detalle = obtener_detalle_por_id(db, id_detalle)
        if not detalle:
            return response_error(
                mensaje=f"No se encontró el detalle con ID {id_detalle}",
                error="DETALLE_NOT_FOUND",
                code=404
            )
        return response_success(
            mensaje="Detalle encontrado",
            data=DetalleOut.model_validate(detalle).model_dump(),
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar el detalle",
            error=str(error),
            code=500
        )