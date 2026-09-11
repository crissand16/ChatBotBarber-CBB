from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db


from app.schema.usuario_schema import (
    LoginRequest, UsuarioCreate
)
from app.controllers.usuario_controller import (
    obtener_clientes,
    obtener_usuarios,
    obtener_especialistas,
    obtener_administradores,
    obtener_usuario,
    registrar_usuario,
    login_usuario
)

from app.utils.response import (
    response_success,
    response_error
)

router = APIRouter(
        prefix="/usuarios", 
        tags=["Usuarios"]
)

# =========================================================
# LISTAR TODOS LOS USUARIOS
# =========================================================

@router.get("")
def listar_usuarios(
    db: Session = Depends(get_db)
):

    try:

        usuarios = obtener_usuarios(db)

        if not usuarios:

            return response_error(
                mensaje="No existen usuarios registrados",
                error="USUARIOS_NOT_FOUND",
                code=404
            )

        data = []

        for usuario in usuarios:

            registro = usuario.copy()

            if registro.get("fecha_registro_usuario"):

                registro["fecha_registro_usuario"] = (
                    registro["fecha_registro_usuario"]
                    .isoformat()
                )

            data.append(registro)

        return response_success(
            mensaje="Usuarios encontrados",
            data=data,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar usuarios",
            error=str(error),
            code=500
        )


# =========================================================
# LISTAR CLIENTES
# =========================================================

@router.get("/clientes")
def listar_clientes(
    db: Session = Depends(get_db)
):

    try:

        clintes = obtener_clientes(db)

        if not clintes:

            return response_error(
                mensaje="No existen clientes registrados",
                error="CLIENTES_NOT_FOUND",
                code=404
            )

        data = []

        for cliente in clintes:

            registro = cliente.copy()

            if registro.get("fecha_registro_usuario"):

                registro["fecha_registro_usuario"] = (
                    registro["fecha_registro_usuario"]
                    .isoformat()
                )

            data.append(registro)

        return response_success(
            mensaje="Clientes encontrados",
            data=data,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar clientes",
            error=str(error),
            code=500
        )


# =========================================================
# LISTAR ESPECIALISTAS
# =========================================================

@router.get("/especialistas")
def listar_especialistas(
    db: Session = Depends(get_db)
):

    try:

        especialistas = obtener_especialistas(db)

        if not especialistas:

            return response_error(
                mensaje="No existen especialistas registrados",
                error="ESPECIALISTAS_NOT_FOUND",
                code=404
            )

        data = []

        for especialista in especialistas:

            registro = especialista.copy()

            if registro.get("fecha_registro_usuario"):

                registro["fecha_registro_usuario"] = (
                    registro["fecha_registro_usuario"]
                    .isoformat()
                )

            data.append(registro)

        return response_success(
            mensaje="Especialistas encontrados",
            data=data,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar especialistas",
            error=str(error),
            code=500
        )


# =========================================================
# LISTAR ADMINISTRADORES
# =========================================================

@router.get("/administradores")
def listar_administradores(
    db: Session = Depends(get_db)
):

    try:

        administradores = obtener_administradores(db)

        if not administradores:

            return response_error(
                mensaje="No existen administradores registrados",
                error="ADMINISTRADORES_NOT_FOUND",
                code=404
            )

        data = []

        for admin in administradores:

            registro = admin.copy()

            if registro.get("fecha_registro_usuario"):

                registro["fecha_registro_usuario"] = (
                    registro["fecha_registro_usuario"]
                    .isoformat()
                )

            data.append(registro)

        return response_success(
            mensaje="Administradores encontrados",
            data=data,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar administradores",
            error=str(error),
            code=500
        )


# =========================================================
# CONSULTAR USUARIO
# =========================================================

@router.get("/{id_usuario}")
def consultar_usuario(
    id_usuario: str,
    db: Session = Depends(get_db)
):

    try:

        usuario = obtener_usuario(
            db,
            id_usuario
        )

        if not usuario:

            return response_error(
                mensaje="El usuario no existe",
                error="USUARIO_NOT_FOUND",
                code=404
            )

        if usuario.get("fecha_registro_usuario"):

            usuario["fecha_registro_usuario"] = (
                usuario["fecha_registro_usuario"]
                .isoformat()
            )

        return response_success(
            mensaje="Usuario encontrado",
            data=usuario,
            code=200
        )

    except Exception as error:

        return response_error(
            mensaje="Error al consultar usuario",
            error=str(error),
            code=500
        )

# =========================================================
# REGISTRAR USUARIO
# =========================================================

@router.post("/registro")
def crear_usuario(
    datos: UsuarioCreate,
    db: Session = Depends(get_db)
):
    try:
        nuevo_usuario = registrar_usuario(db, datos.model_dump())

        if not nuevo_usuario:
            return response_error(
                mensaje="No se pudo registrar el usuario",
                error="USUARIO_CREATE_FAILED",
                code=400
            )

        # Formatear fechas para la respuesta JSON
        data = nuevo_usuario.copy()

        if data.get("fecha_nacimiento_usuario"):
            data["fecha_nacimiento_usuario"] = data["fecha_nacimiento_usuario"].isoformat()

        if data.get("fecha_registro_usuario"):
            data["fecha_registro_usuario"] = data["fecha_registro_usuario"].isoformat()

        return response_success(
            mensaje="Usuario registrado exitosamente",
            data=data,
            code=201
        )

    except Exception as error:
        db.rollback()
        return response_error(
            mensaje="Error al registrar usuario",
            error=str(error),
            code=500
        )

# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):

    try:

        usuario = login_usuario(
            db,
            datos.correo_usuario,
            datos.contrasena_usuario
        )

        # -------------------------------------------------
        # LOGIN INCORRECTO
        # -------------------------------------------------

        if not usuario:

            return response_error(

                mensaje=(
                    "Correo o contraseña incorrectos"
                ),

                error="LOGIN_INVALID",

                code=401,

                data={
                    "logueado": False
                }
            )

        # -------------------------------------------------
        # LOGIN CORRECTO
        # -------------------------------------------------

        return response_success(

            mensaje="Login exitoso",

            data=usuario,

            code=200
        )

    except Exception as error:

        return response_error(

            mensaje="Error al realizar login",

            error=str(error),

            code=500
        )