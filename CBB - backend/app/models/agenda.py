from sqlalchemy import (
Column,
    Integer,
    String,
    ForeignKey,
    Numeric, 
    TIMESTAMP,
    CheckConstraint
)

from sqlalchemy.orm import relationship
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

    __table_args__ = (
        CheckConstraint(
            "estado_agenda IN ('pendiente', 'completada', 'cancelada')",
            name="chk_agenda_estado"
        ),
        CheckConstraint("precio_total >= 0", name="chk_agenda_precio_total"),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    cliente = relationship(
        "Usuario",
        back_populates="agendas_cliente",
        foreign_keys=[id_cliente]
    )

    detalles = relationship(
        "Detalle",
        back_populates="agenda",
        cascade="all, delete-orphan"
    )

    factura = relationship(
        "Factura",
        back_populates="agenda",
        uselist=False
    )

    def __repr__(self):
        return f"<Agenda id={self.id_agenda} estado={self.estado_agenda}>"
