from sqlalchemy import text
from sqlalchemy.orm import Session
 
 
# =========================================================
# LISTAR USUARIOS CON ROL CLIENTE
# =========================================================
 
def obtener_clientes(
    db: Session
):
 
    sql = text("""
        SELECT
            id_usuario,
            nombres_usuario,
            apellidos_usuario,
            correo_usuario,
            fecha_nacimiento_usuario,
            telefono_usuario,
            rol_usuario,
            fecha_registro_usuario
 
        FROM usuario
 
        WHERE rol_usuario = 'cliente'
 
        ORDER BY
            nombres_usuario,
            apellidos_usuario
    """)
 
    resultado = db.execute(sql)
 
    return [
        dict(row._mapping)
        for row in resultado
    ]
 
 
# =========================================================
# LISTAR TODOS LOS USUARIOS
# =========================================================
 
def obtener_usuarios(
    db: Session
):
 
    sql = text("""
        SELECT
 
            u.id_usuario,
            u.nombres_usuario,
            u.apellidos_usuario,
            u.correo_usuario,
            u.fecha_nacimiento_usuario,
            u.telefono_usuario,
            u.rol_usuario,
            u.fecha_registro_usuario
 
        FROM usuario u
 
        ORDER BY
            u.nombres_usuario,
            u.apellidos_usuario
    """)
 
    resultado = db.execute(sql)
 
    return [
        dict(row._mapping)
        for row in resultado
    ]
 
 
# =========================================================
# LISTAR ESPECIALISTAS
# =========================================================
 
def obtener_especialistas(
    db: Session
):
 
    sql = text("""
        SELECT
 
           u.id_usuario,
           u.nombres_usuario,
           u.apellidos_usuario,
           u.correo_usuario,
           u.fecha_nacimiento_usuario,
           u.telefono_usuario,
           u.rol_usuario,
           u.fecha_registro_usuario
 
        FROM usuario u
 
        WHERE u.rol_usuario = 'especialista'
 
        ORDER BY
            u.nombres_usuario,
            u.apellidos_usuario
    """)
 
    resultado = db.execute(sql)
 
    return [
        dict(row._mapping)
        for row in resultado
    ]
 
 
# =========================================================
# LISTAR ADMINISTRADORES
# =========================================================
 
def obtener_administradores(
    db: Session
):
 
    sql = text("""
        SELECT
 
            u.id_usuario,
            u.nombres_usuario,
            u.apellidos_usuario,
            u.correo_usuario,
            u.fecha_nacimiento_usuario,
            u.telefono_usuario,
            u.rol_usuario,
            u.fecha_registro_usuario
 
        FROM usuario u
 
        WHERE u.rol_usuario = 'admin'
 
        ORDER BY
            u.nombres_usuario,
            u.apellidos_usuario
    """)
 
    resultado = db.execute(sql)
 
    return [
        dict(row._mapping)
        for row in resultado
    ]
 
 
# =========================================================
# OBTENER USUARIO POR ID
# =========================================================
 
def obtener_usuario(
    db: Session,
    id_usuario: str
):
 
    sql = text("""
        SELECT
 
            u.id_usuario,
            u.nombres_usuario,
            u.apellidos_usuario,
            u.correo_usuario,
            u.fecha_nacimiento_usuario,
            u.telefono_usuario,
            u.rol_usuario,
            u.fecha_registro_usuario
 
        FROM usuario u
 
        WHERE u.id_usuario = :id_usuario
    """)
 
    resultado = db.execute(
        sql,
        {
            "id_usuario": id_usuario
        }
    ).first()
 
    if not resultado:
        return None
 
    return dict(resultado._mapping)
 
 
# =========================================================
# REGISTRO 
# =========================================================
 
def registrar_usuario(db: Session, datos: dict):
    sql = text("""
        INSERT INTO usuario (
            id_usuario,
            nombres_usuario,
            apellidos_usuario,
            correo_usuario,
            contrasena_usuario,
            fecha_nacimiento_usuario,
            telefono_usuario,
            rol_usuario
        ) VALUES (
            :id_usuario,
            :nombres_usuario,
            :apellidos_usuario,
            :correo_usuario,
            :contrasena_usuario,
            :fecha_nacimiento_usuario,
            :telefono_usuario,
            :rol_usuario
        )
        RETURNING 
            id_usuario,
            nombres_usuario,
            apellidos_usuario,
            correo_usuario,
            fecha_nacimiento_usuario,
            telefono_usuario,
            rol_usuario,
            fecha_registro_usuario
    """)
 
    resultado = db.execute(sql, datos).first()
    db.commit()
 
    if not resultado:
        return None
 
    return dict(resultado._mapping)
 
# =========================================================
# LOGIN SIMPLE
# =========================================================
 
def login_usuario(
    db: Session,
    correo_usuario: str,
    contrasena_usuario: str
):
 
    sql = text("""
        SELECT
 
            id_usuario,
            nombres_usuario,
            apellidos_usuario,
            correo_usuario,
            contrasena_usuario,
            rol_usuario
 
        FROM usuario
 
        WHERE correo_usuario = :correo_usuario
    """)
 
    resultado = db.execute(
        sql,
        {
            "correo_usuario": correo_usuario
        }
    ).first()
 
    # -----------------------------------------------------
    # USUARIO NO EXISTE
    # -----------------------------------------------------
 
    if not resultado:
 
        return None
 
    # -----------------------------------------------------
    # VALIDAR CONTRASEÑA
    # -----------------------------------------------------
 
    if resultado.contrasena_usuario != contrasena_usuario:
 
        return None
 
    # -----------------------------------------------------
    # LOGIN CORRECTO
    # -----------------------------------------------------
 
    return {
        "logueado": True,
 
        "id_usuario":
            resultado.id_usuario,
 
        "nombres":
            resultado.nombres_usuario,
 
        "apellidos":
            resultado.apellidos_usuario,
 
        "correo":
            resultado.correo_usuario,
 
        "rol":
            resultado.rol_usuario,
 
    }
 