from datetime import date

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import get_db

from app.schema.disponibilidad_schema import (
    DisponibilidadCreate,
    DisponibilidadUpdate,
    DisponibilidadOut
)

from app.controllers.disponibilidad_controller import (
    obtener_disponibilidad_especialista,
    obtener_disponibilidad_rango,
    crear_disponibilidad,
    actualizar_disponibilidad,
    obtener_disponibilidad_por_id
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


# =========================================================
# 3. CREAR UN BLOQUE DE DISPONIBILIDAD
# =========================================================

@router.post("")
def registrar_disponibilidad(
    datos: DisponibilidadCreate,
    db: Session = Depends(get_db)
):
    try:
        nueva = crear_disponibilidad(db, datos.model_dump())
        return response_success(
            mensaje="Disponibilidad registrada exitosamente",
            data=DisponibilidadOut.model_validate(nueva).model_dump(),
            code=201
        )
    except ValueError as error:
        db.rollback()
        return response_error(
            mensaje=str(error),
            error="DISPONIBILIDAD_VALIDATION_ERROR",
            code=400
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al registrar la disponibilidad",
            error=str(error),
            code=500
        )


# =========================================================
# 4. ACTUALIZAR UN BLOQUE DE DISPONIBILIDAD
# =========================================================

@router.patch("/{id_disponibilidad}")
def modificar_disponibilidad(
    id_disponibilidad: int,
    datos: DisponibilidadUpdate,
    db: Session = Depends(get_db)
):
    try:
        actualizada = actualizar_disponibilidad(
            db,
            id_disponibilidad,
            datos.model_dump(exclude_unset=True)
        )
        return response_success(
            mensaje="Disponibilidad actualizada exitosamente",
            data=DisponibilidadOut.model_validate(actualizada).model_dump(),
            code=200
        )
    except ValueError as error:
        db.rollback()
        code = 404 if "no existe" in str(error) else 400
        return response_error(
            mensaje=str(error),
            error="DISPONIBILIDAD_UPDATE_FAILED",
            code=code
        )
    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al actualizar la disponibilidad",
            error=str(error),
            code=500
        )


# =========================================================
# 5. OBTENER UN BLOQUE DE DISPONIBILIDAD POR ID
# =========================================================

@router.get("/{id_disponibilidad}")
def obtener_por_id(
    id_disponibilidad: int,
    db: Session = Depends(get_db)
):
    try:
        disponibilidad = obtener_disponibilidad_por_id(db, id_disponibilidad)
        if not disponibilidad:
            return response_error(
                mensaje=f"No se encontró la disponibilidad con ID {id_disponibilidad}",
                error="DISPONIBILIDAD_NOT_FOUND",
                code=404
            )
        return response_success(
            mensaje="Disponibilidad encontrada",
            data=DisponibilidadOut.model_validate(disponibilidad).model_dump(),
            code=200
        )
    except Exception as error:
        return response_error(
            mensaje="Error al consultar la disponibilidad",
            error=str(error),
            code=500
        )
