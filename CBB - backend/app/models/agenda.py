from sqlalchemy import (
Column,
    Integer,
    String,
    ForeignKey,
    Numeric, 
    TIMESTAMP
)

from app.config.database import Base


class Agenda(Base):

    __tablename__ = "agenda"

    id_agenda = Column( 
        Integer,
        primary_key=True
    )

    id_cliente = Column(
        String(10),
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    estado_agenda = Column(
        String(20),
        nullable=False
    )

    precio_total = Column(
        Numeric(10, 2),
        nullable=False
    )

    fecha_creacion_agenda = Column(
        TIMESTAMP,
        nullable=False
    )
