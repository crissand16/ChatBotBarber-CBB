from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.usuario import Usuario

from passlib.context import CryptContext

from app.models.agenda import Agenda
from app.models.detalle import Detalle
from app.models.disponibilidad import Disponibilidad
from app.models.servicio_disponibilidad import ServicioDisponibilidad
from app.models.usuario import Usuario
from app.utils.errores import Conflicto, NoEncontrado


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

    # 1. Obtener la contraseña en texto plano y generar su hash
    contrasena_plana = datos["contrasena_usuario"]
    contrasena_hash = pwd_context.hash(contrasena_plana)
    nuevo = Usuario(
        id_usuario=datos["id_usuario"],
        nombres_usuario=datos["nombres_usuario"],
        apellidos_usuario=datos["apellidos_usuario"],
        correo_usuario=datos["correo_usuario"],
        contrasena_usuario=contrasena_hash, #Se almacena el hash y no la contraseña plana
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


    if not pwd_context.verify(contrasena_usuario, usuario.contrasena_usuario):
        return None

    return {
        "logueado": True,
        "id_usuario": usuario.id_usuario,
        "nombres": usuario.nombres_usuario,
        "apellidos": usuario.apellidos_usuario,
        "correo": usuario.correo_usuario,
        "rol": usuario.rol_usuario,
    }


# =========================================================
# HELPER: BUSCAR UN USUARIO POR ID Y ROL
# =========================================================

def _obtener_con_rol(db: Session, id_usuario: str, rol: str) -> Usuario:
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id_usuario == id_usuario, Usuario.rol_usuario == rol)
        .first()
    )

    if not usuario:
        raise NoEncontrado(f"No existe un {rol} con ID {id_usuario}")

    return usuario


# =========================================================
# EDITAR PERFIL
# =========================================================
# Solo se modifican los campos que llegan con valor. El rol, el id y la
# contraseña no se pueden cambiar desde aquí.
 
campos_perfil = (
    "nombres_usuario",
    "apellidos_usuario",
    "correo_usuario",
    "telefono_usuario",
    "fecha_nacimiento_usuario",
)

def actualizar_perfil(db: Session, id_usuario: Usuario, datos: dict, rol:str ) -> Usuario:
    usuario = _obtener_con_rol(db, id_usuario, rol)

    cambios = {c: datos[c] for c in campos_perfil if datos.get(c) is not None}
    if not cambios:
        raise ValueError("No se enviaron campos para actualizar")
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    try:
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError:
        db.rollback()
        raise Conflicto("Ya existe otro usuario con este correo electrónico")


# =========================================================
# DESACTIVAR ESPECIALISTA (borrado lógico)
# =========================================================
# No se borra la fila: se conserva el historial de agendas y facturas.
# Se bloquea si el especialista tiene citas futuras pendientes o aceptadas,
# para no dejar clientes con una cita sin especialista.

def desactivar_especialista(db: Session, id_usuario: str) -> Usuario:
    especialista = _obtener_con_rol(db, id_usuario, "especialista")

    # if not especialista.activo:
    #     raise Conflicto("El especialista ya está desactivado")

    citas_futuras = (
        db.query(func.count(func.distinct(Agenda.id_agenda)))
        .select_from(Agenda)
        .join(Detalle, Detalle.id_agenda == Agenda.id_agenda)
        .join(
            ServicioDisponibilidad,
            ServicioDisponibilidad.id_servicio_disponibilidad
            == Detalle.id_servicio_disponibilidad,
        )
        .join(
            Disponibilidad,
            Disponibilidad.id_disponibilidad == ServicioDisponibilidad.id_disponibilidad,
        )
        .filter(
            Disponibilidad.id_especialista == id_usuario,
            Disponibilidad.fecha_disponibilidad >= date.today(),
            Agenda.estado_agenda.in_(("pendiente", "aceptada")),
        )
        .scalar()
    )

    if citas_futuras:
        raise Conflicto(
            f"El especialista tiene {citas_futuras} cita(s) futura(s) pendientes o aceptadas. "
            "Cancélalas antes de desactivarlo"
        )

   
    db.commit()
    db.refresh(especialista)
    return especialista
