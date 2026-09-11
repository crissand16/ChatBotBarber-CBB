from datetime import date

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.controllers.disponibilidad_controller import (
    obtener_disponibilidad_especialista,
    obtener_disponibilidad_rango
)

from app.utils.response import (
    response_success,
    response_error
) 


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/disponibilidad",
    tags=["Disponibilidad"]
)


# =========================================================
# 1. TODA LA DISPONIBILIDAD DE UN ESPECIALISTA
# =========================================================

@router.get(
    "/especialista/{id_especialista}"
)
def disponibilidad_especialista(

    id_especialista: str,

    db: Session = Depends(get_db)

):

    try:

        # -------------------------------------------------
        # CONSULTAR DISPONIBILIDAD
        # -------------------------------------------------

        datos = obtener_disponibilidad_especialista(
            db,
            id_especialista
        )

        # -------------------------------------------------
        # VALIDAR RESULTADO
        # -------------------------------------------------

        if not datos:

            return response_error(

                mensaje=(
                    "El especialista no tiene "
                    "disponibilidad registrada"
                ),

                error="DISPONIBILIDAD_NOT_FOUND",

                code=404

            )

        # -------------------------------------------------
        # RESPUESTA
        # -------------------------------------------------

        return response_success(

            mensaje=(
                "Disponibilidad del especialista encontrada"
            ),

            data=datos,

            code=200

        )

    except Exception as error:

        return response_error(

            mensaje=(
                "Error al consultar la disponibilidad "
                "del especialista"
            ),

            error=str(error),

            code=500

        )


# =========================================================
# 2. DISPONIBILIDAD DE TODOS LOS ESPECIALISTAS
#    ENTRE DOS FECHAS
# =========================================================

@router.get("")
def disponibilidad_rango(

    fecha_inicio: date,

    fecha_fin: date,

    db: Session = Depends(get_db)

):

    try:

        # -------------------------------------------------
        # VALIDAR RANGO DE FECHAS
        # -------------------------------------------------

        if fecha_inicio > fecha_fin:

            return response_error(

                mensaje=(
                    "La fecha inicial no puede ser "
                    "mayor que la fecha final"
                ),

                error="INVALID_DATE_RANGE",

                code=400

            )

        # -------------------------------------------------
        # CONSULTAR DISPONIBILIDAD
        # -------------------------------------------------

        datos = obtener_disponibilidad_rango(

            db,

            fecha_inicio,

            fecha_fin

        )

        # -------------------------------------------------
        # VALIDAR RESULTADO
        # -------------------------------------------------

        if not datos:

            return response_error(

                mensaje=(
                    "No existe disponibilidad "
                    "en el rango de fechas indicado"
                ),

                error="DISPONIBILIDAD_NOT_FOUND",

                code=404

            )

        # -------------------------------------------------
        # RESPUESTA
        # -------------------------------------------------

        return response_success(

            mensaje=(
                "Disponibilidad encontrada para "
                "todos los especialistas"
            ),

            data=datos,

            code=200

        )

    except Exception as error:

        return response_error(

            mensaje=(
                "Error al consultar la disponibilidad"
            ),

            error=str(error),

            code=500

        )