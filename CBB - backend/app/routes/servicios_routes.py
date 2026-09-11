from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schema.servicios_schema import ServicioCreate, ServicioUpdate
from app.controllers.servicios_controller import (
    listar_servicios,
    obtener_servicio_por_id,
    crear_servicio
)
from app.utils.response import response_success, response_error

router = APIRouter(
    prefix="/servicios",
    tags=["Servicios"]
)

# =========================================================
# LISTAR TODOS LOS SERVICIOS
# =========================================================
@router.get("")
def obtener_todos(db: Session = Depends(get_db)):
    try:
        servicios = listar_servicios(db)
        if not servicios:
            return response_error(
                mensaje="No existen servicios registrados",
                error="SERVICIOS_NOT_FOUND",
                code=404
            )
        
        # Convertir precio Decimal a float estandar en Python 
        data = []
        for s in servicios:
            item = s.copy()
            if item.get("precio_servicio") is not None:
                item["precio_servicio"] = float(item["precio_servicio"])
            data.append(item)

        return response_success(
            mensaje="Servicios obtenidos exitosamente",
            data=data,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar servicios",
            error=str(error),
            code=500
        )

# =========================================================
# OBTENER SERVICIO POR ID
# =========================================================
@router.get("/{id_servicio}")
def obtener_por_id(id_servicio: int, db: Session = Depends(get_db)):
    try:
        servicio = obtener_servicio_por_id(db, id_servicio)
        if not servicio:
            return response_error(
                mensaje=f"No se encontró el servicio con ID {id_servicio}",
                error="SERVICIO_NOT_FOUND",
                code=404
            )
        
        data = servicio.copy()
        if data.get("precio_servicio") is not None:
            data["precio_servicio"] = float(data["precio_servicio"])

        return response_success(
            mensaje="Servicio encontrado",
            data=data,
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al obtener el servicio",
            error=str(error),
            code=500
        )

# =========================================================
# CREAR UN NUEVO SERVICIO
# =========================================================
@router.post("")
def registrar_servicio(datos: ServicioCreate, db: Session = Depends(get_db)):
    try:
        nuevo_servicio = crear_servicio(db, datos.model_dump())
        if not nuevo_servicio:
            return response_error(
                mensaje="No se pudo registrar el servicio",
                error="SERVICIO_CREATE_FAILED",
                code=400
            )

        data = nuevo_servicio.copy()
        if data.get("precio_servicio") is not None:
            data["precio_servicio"] = float(data["precio_servicio"])

        return response_success(
            mensaje="Servicio creado exitosamente",
            data=data,
            code=201
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al registrar el servicio",
            error=str(error),
            code=500
        )


