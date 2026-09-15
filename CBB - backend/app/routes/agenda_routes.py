from datetime import date
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.models.agenda import Agenda
from app.models.detalle import Detalle

from app.schema.agenda_schema import (
    AgendaCreate,
    AgendaUpdateEstado
)

from app.controllers.agenda_controller import (
    obtener_agendas,
    crear_agenda,
    obtener_citas_especialista,
    obtener_agendas_por_cliente,
    obtener_agendas_por_fecha,
    cancelar_agenda
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
# LISTAR TODAS LAS AGENDAS
# =========================================================

@router.get("")
def listar_agendas(db: Session = Depends(get_db)):
    try:
        agendas = obtener_agendas(db)

        if not agendas:
            return response_error(
                mensaje="No hay registros en la agenda",
                error="AGENDA_EMPTY",
                code=404
            )

        return response_success(
            mensaje="Agendas consultadas correctamente",
            data=agendas,
            code=200
        )

    except Exception as error:
        return response_error(
            mensaje="Error al consultar la agenda",
            error=str(error),
            code=500
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


# =========================================================
# CAMBIAR ESTADO DE UNA AGENDA
# =========================================================

@router.patch("/{id_agenda}/estado")
def cambiar_estado_agenda(
    id_agenda: int,
    payload: AgendaUpdateEstado, #datos reales que se envían entre el cliente y el servidor
    db: Session = Depends(get_db)
):
    try:
        # 1. Buscar la agenda existente (ORM)
        agenda = db.query(Agenda).filter(Agenda.id_agenda == id_agenda).first()

        if not agenda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La agenda con ID {id_agenda} no fue encontrada."
            )

        nuevo_estado = payload.nuevo_estado.lower().strip()
        agenda.estado_agenda = nuevo_estado

        # 2. Si la agenda se cancela, liberar la disponibilidad asociada
        #    Se navega por las relaciones del ORM en vez de SQL crudo:
        #    Agenda -> Detalle -> ServicioDisponibilidad -> Disponibilidad
        if nuevo_estado == "cancelada":
            detalles = (
                db.query(Detalle)
                .filter(Detalle.id_agenda == id_agenda)
                .all()
            )

            for detalle in detalles:
                servicio_disponibilidad = detalle.servicio_disponibilidad
                if servicio_disponibilidad and servicio_disponibilidad.disponibilidad:
                    servicio_disponibilidad.disponibilidad.estado_disponibilidad = "disponible"

        # 3. Guardar cambios en la base de datos
        db.commit()
        db.refresh(agenda)

        return response_success(
            mensaje=f"Estado de la agenda actualizado a '{nuevo_estado}' exitosamente.",
            data={
                "id_agenda": agenda.id_agenda,
                "estado_agenda": agenda.estado_agenda
            },
            code=200
        )

    except HTTPException as http_exc:
        db.rollback()
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el estado de la agenda: {str(e)}"
        )


# =========================================================
# ANULAR (CANCELAR) UNA AGENDA
# =========================================================

@router.delete("/{id_agenda}")
def anular_agenda(id_agenda: int, db: Session = Depends(get_db)):
    try:
        cancelada = cancelar_agenda(db, id_agenda)

        if not cancelada:
            return response_error(
                mensaje="Agenda no encontrada",
                error="AGENDA_NOT_FOUND",
                code=404
            )

        return response_success(
            mensaje="Cita/Agenda cancelada exitosamente",
            code=200
        )

    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al cancelar la agenda",
            error=str(error),
            code=500
        )
