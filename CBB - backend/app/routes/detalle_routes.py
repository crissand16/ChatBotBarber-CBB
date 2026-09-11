from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.detalle import DetalleCreate
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
        if not nuevo:
            return response_error(
                mensaje="No se pudo registrar el detalle de la agenda",
                error="DETALLE_CREATE_FAILED",
                code=400
            )
        return response_success(
            mensaje="Detalle registrado exitosamente",
            data=nuevo,
            code=201
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
        return response_success(
            mensaje="Lista de detalles obtenida con éxito",
            data=registros,
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
            data=detalle,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar el detalle",
            error=str(error),
            code=500
        )