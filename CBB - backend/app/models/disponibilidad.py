from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    ForeignKey
)

from app.config.database import Base


class Disponibilidad(Base):

    __tablename__ = "disponibilidad"

    id_disponibilidad = Column(
        Integer,
        primary_key=True
    )

    id_usuario = Column(
        String(10),
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    fecha_disponibilidad = Column(
        Date,
        nullable=False
    )

    hora_inicio_disponibilidad = Column(
        Time,
        nullable=False
    )

    hora_fin_disponibilidad = Column(
        Time,
        nullable=False
    )

    estado_disponibilidad = Column(
        String(20),
        nullable=False
    )