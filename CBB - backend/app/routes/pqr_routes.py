from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.controllers.pqr_controller import crear_pqr
from app.schema.pqr_schema import PqrCreate, PqrOut
from app.utils.errores import NoEncontrado
from app.utils.response import response_success, response_error

router = APIRouter(
    prefix="/pqr",
    tags=["PQR"]
)


# =========================================================
# RADICAR UNA PQR (petición, queja o reclamo)
# =========================================================

@router.post("")
def registrar_pqr(datos: PqrCreate, db: Session = Depends(get_db)):
    try:
        pqr = crear_pqr(db, datos.model_dump())

        if pqr.correo_enviado_pqr:
            mensaje = (
                f"Tu solicitud fue radicada con el número {pqr.radicado}. "
                "Te responderemos a tu correo."
            )
        else:
            mensaje = (
                f"Tu solicitud fue radicada con el número {pqr.radicado}, "
                "pero no pudimos enviar la notificación por correo. "
                "El equipo la revisará igualmente."
            )

        return response_success(
            mensaje=mensaje,
            data=PqrOut.model_validate(pqr).model_dump(),
            code=201
        )

    except NoEncontrado as error:
        db.rollback()
        return response_error(
            mensaje=str(error),
            error="USUARIO_NOT_FOUND",
            code=404
        )

    except ValueError as error:
        db.rollback()
        return response_error(
            mensaje=str(error),
            error="PQR_VALIDATION_ERROR",
            code=400
        )

    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al registrar la PQR",
            error=str(error),
            code=500
        )
