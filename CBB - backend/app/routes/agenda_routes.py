from datetime import date
from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schema.agenda_schema import (
    AgendaCreate
)

from app.controllers.agenda_controller import (
    crear_agenda,
    obtener_citas_especialista,
    obtener_agendas_por_cliente,
    obtener_agendas_por_fecha
)

from app.utils.response import ( 
    response_success,
    response_error
)


router = APIRouter(
    prefix="/agendas",
    tags=["Agendas"]
)


# =========================================================
# CREAR AGENDA
# =========================================================

@router.post("")
def registrar_agenda(
    datos: AgendaCreate,
    db: Session = Depends(get_db)
):

    try:

        agenda = crear_agenda(
            db,
            datos
        )

        return response_success(
            mensaje="Agenda creada correctamente",
            data={
                "id_agenda": agenda.id_agenda,
                "id_cliente": agenda.id_cliente,
                "estado_agenda": agenda.estado_agenda,
                "precio_total": float(agenda.precio_total),
                "fecha_creacion_agenda": (
                    agenda.fecha_creacion_agenda.isoformat()
                    if agenda.fecha_creacion_agenda
                    else None
                )
            },
            code=201
        )

    except ValueError as error:

        db.rollback()

        return response_error(
            mensaje=str(error),
            error="AGENDA_VALIDATION_ERROR",
            code=400
        )

    except Exception as error:

        db.rollback()

        return response_error(
            mensaje="Error al crear la agenda",
            error=str(error),
            code=500
        )


# =========================================================
# AGENDAS POR ESPECIALISTA
# =========================================================

@router.get(
    "/especialista/{id_especialista}"
)
def agendas_por_especialista(

    id_especialista: str,

    db: Session = Depends(get_db)

):

    try:

        datos = obtener_citas_especialista(
            db,
            id_especialista
        )

        if not datos:

            return response_error(
                mensaje="El especialista no tiene agendas registradas",
                error="AGENDAS_NOT_FOUND",
                code=404
            )

        return response_success(
            mensaje="Agendas del especialista encontradas",
            data=datos,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar las agendas del especialista",
            error=str(error),
            code=500
        )


# =========================================================
# AGENDAS POR CLIENTE
# =========================================================

@router.get(
    "/cliente/{id_cliente}"
)
def agendas_por_cliente(

    id_cliente: str,

    db: Session = Depends(get_db)

):

    try:

        datos = obtener_agendas_por_cliente(
            db,
            id_cliente
        )

        if not datos:

            return response_error(
                mensaje="El cliente no tiene agendas registradas",
                error="AGENDAS_NOT_FOUND",
                code=404
            )

        return response_success(
            mensaje="Agendas del cliente encontradas",
            data=datos,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar las agendas del cliente",
            error=str(error),
            code=500
        )


# =========================================================
# AGENDAS POR FECHA
# =========================================================

@router.get(
    "/fecha/{fecha}"
)
def agendas_por_fecha(

    fecha: date,

    db: Session = Depends(get_db)

):

    try:

        datos = obtener_agendas_por_fecha(
            db,
            str(fecha)
        )

        if not datos:

            return response_error(
                mensaje="No existen agendas para la fecha indicada",
                error="AGENDAS_NOT_FOUND",
                code=404
            )

        return response_success(
            mensaje="Agendas encontradas para la fecha",
            data=datos,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar las agendas por fecha",
            error=str(error),
            code=500
        )