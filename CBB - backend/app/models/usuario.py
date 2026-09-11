from sqlalchemy import Column, String, TIMESTAMP, Date

from app.config.database import Base


class Usuario(Base):

    __tablename__ = "usuario"

    id_usuario = Column(
        String(10),
        primary_key=True
    )

    nombres_usuario = Column(
        String(40),
        nullable=False
    )

    apellidos_usuario = Column(
        String(40),
        nullable=False
    )

    correo_usuario = Column(
        String(60),
        nullable=False,
        unique=True
    )

    contrasena_usuario = Column(
        String(255),
        nullable=False
    )

    fecha_nacimiento_usuario = Column(
        Date,
        nullable=False
    )

    telefono_usuario = Column(
        String(20)
    )

    rol_usuario = Column(
        String(20),
        nullable=False
    )

    fecha_registro_usuario = Column(
        TIMESTAMP,
        nullable=False
    )