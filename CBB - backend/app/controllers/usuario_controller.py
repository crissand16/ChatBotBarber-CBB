from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.usuario import Usuario


# =========================================================
# LISTAR USUARIOS CON ROL CLIENTE
# =========================================================

def obtener_clientes(db: Session):
    return (
        db.query(Usuario)
        .filter(Usuario.rol_usuario == "cliente")
        .order_by(Usuario.nombres_usuario, Usuario.apellidos_usuario)
        .all()
    )


# =========================================================
# LISTAR TODOS LOS USUARIOS
# =========================================================

def obtener_usuarios(db: Session):
    return (
        db.query(Usuario)
        .order_by(Usuario.nombres_usuario, Usuario.apellidos_usuario)
        .all()
    )


# =========================================================
# LISTAR ESPECIALISTAS
# =========================================================

def obtener_especialistas(db: Session):
    return (
        db.query(Usuario)
        .filter(Usuario.rol_usuario == "especialista")
        .order_by(Usuario.nombres_usuario, Usuario.apellidos_usuario)
        .all()
    )


# =========================================================
# LISTAR ADMINISTRADORES
# =========================================================

def obtener_administradores(db: Session):
    return (
        db.query(Usuario)
        .filter(Usuario.rol_usuario == "admin")
        .order_by(Usuario.nombres_usuario, Usuario.apellidos_usuario)
        .all()
    )


# =========================================================
# OBTENER USUARIO POR ID
# =========================================================

def obtener_usuario(db: Session, id_usuario: str):
    return (
        db.query(Usuario)
        .filter(Usuario.id_usuario == id_usuario)
        .first()
    )


# =========================================================
# REGISTRO
# =========================================================

def registrar_usuario(db: Session, datos: dict):
    nuevo = Usuario(
        id_usuario=datos["id_usuario"],
        nombres_usuario=datos["nombres_usuario"],
        apellidos_usuario=datos["apellidos_usuario"],
        tipo_documento_usuario=datos.get("tipo_documento_usuario") or "CC",
        documento_usuario=datos["documento_usuario"],
        correo_usuario=datos["correo_usuario"],
        contrasena_usuario=datos["contrasena_usuario"],
        fecha_nacimiento_usuario=datos["fecha_nacimiento_usuario"],
        telefono_usuario=datos["telefono_usuario"],
        rol_usuario=datos.get("rol_usuario") or "cliente"
    )

    try:
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Ya existe un usuario con ese id_usuario, "
            "documento_usuario o correo_usuario"
        )


# =========================================================
# LOGIN SIMPLE
# =========================================================

def login_usuario(db: Session, correo_usuario: str, contrasena_usuario: str):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.correo_usuario == correo_usuario)
        .first()
    )

    if not usuario:
        return None

    if usuario.contrasena_usuario != contrasena_usuario:
        return None

    return {
        "logueado": True,
        "id_usuario": usuario.id_usuario,
        "nombres": usuario.nombres_usuario,
        "apellidos": usuario.apellidos_usuario,
        "correo": usuario.correo_usuario,
        "rol": usuario.rol_usuario,
    }
