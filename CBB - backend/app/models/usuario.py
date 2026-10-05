from sqlalchemy import Column, String, TIMESTAMP, Date, CheckConstraint

from sqlalchemy.orm import relationship
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

    __table_args__ = (
        CheckConstraint(
            "tipo_documento_usuario IN ('TI', 'CC', 'PPT')",
            name="chk_usuario_tipo_documento"
        ),
        CheckConstraint(
            "rol_usuario IN ('cliente', 'especialista', 'admin')",
            name="chk_usuario_rol"
        ),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    # Agendas donde este usuario es el cliente que agenda la cita
    agendas_cliente = relationship(
        "Agenda",
        back_populates="cliente",
        foreign_keys="Agenda.id_cliente"
    )

    # Bloques de disponibilidad donde este usuario es el especialista
    disponibilidades = relationship(
        "Disponibilidad",
        back_populates="especialista",
        foreign_keys="Disponibilidad.id_especialista",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario id={self.id_usuario} rol={self.rol_usuario}>"
