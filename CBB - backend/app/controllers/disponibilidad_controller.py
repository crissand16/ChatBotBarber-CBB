from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.models.disponibilidad import Disponibilidad
from app.models.usuario import Usuario


# =========================================================
# HELPER: SERIALIZAR UN REGISTRO DE DISPONIBILIDAD
# =========================================================
# Mantiene la misma forma de dict que antes devolvía el SQL

def _serializar(disponibilidad: Disponibilidad) -> dict:
    return {
        "id_disponibilidad": disponibilidad.id_disponibilidad,
        "id_especialista": disponibilidad.id_especialista,
        "nombres_usuario": disponibilidad.especialista.nombres_usuario,
        "apellidos_usuario": disponibilidad.especialista.apellidos_usuario,
        "fecha_disponibilidad": disponibilidad.fecha_disponibilidad,
        "hora_inicio_disponibilidad": disponibilidad.hora_inicio_disponibilidad,
        "hora_fin_disponibilidad": disponibilidad.hora_fin_disponibilidad,
        "estado_disponibilidad": disponibilidad.estado_disponibilidad,
    }


# =========================================================
# OBTENER TODA LA DISPONIBILIDAD DE UN ESPECIALISTA
# =========================================================

def obtener_disponibilidad_especialista(db: Session, id_especialista: str):
    registros = (
        db.query(Disponibilidad)
        .options(joinedload(Disponibilidad.especialista))
        .filter(Disponibilidad.id_especialista == id_especialista)
        .order_by(
            Disponibilidad.fecha_disponibilidad,
            Disponibilidad.hora_inicio_disponibilidad
        )
        .all()
    )
    return [_serializar(d) for d in registros]


# =========================================================
# OBTENER DISPONIBILIDAD DE TODOS LOS ESPECIALISTAS
# ENTRE DOS FECHAS
# =========================================================

def obtener_disponibilidad_rango(db: Session, fecha_inicio, fecha_fin):
    registros = (
        db.query(Disponibilidad)
        .join(Usuario, Disponibilidad.id_especialista == Usuario.id_usuario)
        .options(joinedload(Disponibilidad.especialista))
        .filter(Usuario.rol_usuario == "especialista")
        .filter(Disponibilidad.fecha_disponibilidad.between(fecha_inicio, fecha_fin))
        .order_by(
            Disponibilidad.fecha_disponibilidad,
            Usuario.nombres_usuario,
            Usuario.apellidos_usuario,
            Disponibilidad.hora_inicio_disponibilidad
        )
        .all()
    )
    return [_serializar(d) for d in registros]


# =========================================================
# CREAR UN BLOQUE DE DISPONIBILIDAD
# =========================================================

def crear_disponibilidad(db: Session, datos: dict):
    especialista = (
        db.query(Usuario)
        .filter(Usuario.id_usuario == datos["id_especialista"])
        .first()
    )

    if not especialista:
        raise ValueError("El especialista indicado no existe")

    if especialista.rol_usuario != "especialista":
        raise ValueError("El usuario indicado no tiene rol de especialista")

    nueva = Disponibilidad(
        id_especialista=datos["id_especialista"],
        fecha_disponibilidad=datos["fecha_disponibilidad"],
        hora_inicio_disponibilidad=datos["hora_inicio_disponibilidad"],
        hora_fin_disponibilidad=datos["hora_fin_disponibilidad"],
        estado_disponibilidad=datos.get("estado_disponibilidad") or "disponible"
    )

    try:
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "El especialista ya tiene un bloque de disponibilidad "
            "registrado en esa fecha y hora de inicio"
        )


# =========================================================
# ACTUALIZAR UN BLOQUE DE DISPONIBILIDAD (parcial)
# =========================================================

def actualizar_disponibilidad(db: Session, id_disponibilidad: int, datos: dict):
    disponibilidad = (
        db.query(Disponibilidad)
        .filter(Disponibilidad.id_disponibilidad == id_disponibilidad)
        .first()
    )

    if not disponibilidad:
        raise ValueError("La disponibilidad indicada no existe")

    campos_actualizables = (
        "fecha_disponibilidad",
        "hora_inicio_disponibilidad",
        "hora_fin_disponibilidad",
        "estado_disponibilidad"
    )

    for campo in campos_actualizables:
        if datos.get(campo) is not None: #get  obtiene el valor de una clave  
            setattr(disponibilidad, campo, datos[campo])

    try:
        db.commit()
        db.refresh(disponibilidad) #Vuelve a leer el objeto desde la base
        return disponibilidad
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "El especialista ya tiene un bloque de disponibilidad "
            "registrado en esa fecha y hora de inicio"
        )


# =========================================================
# OBTENER UN BLOQUE DE DISPONIBILIDAD POR ID
# =========================================================

def obtener_disponibilidad_por_id(db: Session, id_disponibilidad: int):
    return (
        db.query(Disponibilidad)
        .filter(Disponibilidad.id_disponibilidad == id_disponibilidad)
        .first()
    )
