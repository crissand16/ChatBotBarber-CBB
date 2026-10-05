from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schema.servi_dispo_schema import (
    ServicioDisponibilidadCreate,
    ServicioDisponibilidadOut
)

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
        return response_success(
            mensaje="Servicio y disponibilidad asociados exitosamente",
            data=ServicioDisponibilidadOut.model_validate(nuevo).model_dump(),
            code=201
        )
    except ValueError as error:
        db.rollback()
        return response_error(
            mensaje=str(error) or "No se pudo asociar el servicio con la disponibilidad",
            error="ASOCIACION_FAILED",
            code=400
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
        # BUG anterior: "module_validate" no existe en Pydantic (el método se
        # llama "model_validate"); ese typo hacía que ESTE endpoint fallara
        # siempre con un error 500. Como "Agendar nueva cita" llama a este
        # endpoint apenas el cliente elige un servicio (para saber qué
        # franjas de disponibilidad están habilitadas para ese servicio),
        # el error se disparaba en el primer paso del flujo de agendamiento.
        data = [ServicioDisponibilidadOut.model_validate(r).model_dump() for r in registros]
        return response_success(
            mensaje="Lista de servicio_disponibilidad obtenida con éxito",
            data=data,
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
            # BUG anterior: faltaban los "()" tras model_dump, así que se
            # devolvía el método en sí (no serializable a JSON) en vez de
            # los datos.
            data=ServicioDisponibilidadOut.model_validate(registro).model_dump(),
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar el registro",
            error=str(error),
            code=500
        )