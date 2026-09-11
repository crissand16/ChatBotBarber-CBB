from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.servicio_disponibilidad import ServicioDisponibilidadCreate
from app.controllers.servi_dispo_controller import (
    crear_servicio_disponibilidad,
    obtener_servicio_disponibilidad,
    obtener_servicio_disponibilidad_por_id
)
from app.utils.response import response_success, response_error

router = APIRouter(
    prefix="/servicio_disponibilidad",
    tags=["Servicio Disponibilidad"]
)

@router.post("")
def registrar(datos: ServicioDisponibilidadCreate, db: Session = Depends(get_db)):
    try:
        nuevo = crear_servicio_disponibilidad(db, datos.model_dump())
        if not nuevo:
            return response_error(
                mensaje="No se pudo asociar el servicio con la disponibilidad",
                error="ASOCIACION_FAILED",
                code=400
            )
        return response_success(
            mensaje="Servicio y disponibilidad asociados exitosamente",
            data=nuevo,
            code=201
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al asociar servicio y disponibilidad",
            error=str(error),
            code=500
        )

@router.get("")
def listar_todos(db: Session = Depends(get_db)):
    try:
        registros = obtener_servicio_disponibilidad(db)
        return response_success(
            mensaje="Lista de servicio_disponibilidad obtenida con éxito",
            data=registros,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al obtener la lista de registros",
            error=str(error),
            code=500
        ) 

@router.get("/{servicio_disponibilidad}")
def obtener_por_id(servicio_disponibilidad: int, db: Session = Depends(get_db)):
    try:
        registro = obtener_servicio_disponibilidad_por_id(db, servicio_disponibilidad)
        if not registro:
            return response_error(
                mensaje=f"No se encontró el registro con ID {servicio_disponibilidad}",
                error="REGISTRO_NOT_FOUND",
                code=404
            )
        return response_success(
            mensaje="Registro encontrado",
            data=registro,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar el registro",
            error=str(error),
            code=500
        )