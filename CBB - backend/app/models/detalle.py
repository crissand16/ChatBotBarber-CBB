from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.config.database import Base


class Detalle(Base):
    """
    Línea de detalle de una agenda: une una agenda con un
    servicio_disponibilidad puntual (un servicio en un horario concreto).
    """

    __tablename__ = "detalle"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)

    id_agenda = Column(
        Integer,
        ForeignKey("agenda.id_agenda", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    id_servicio_disponibilidad = Column(
        Integer,
        ForeignKey("servicio_disponibilidad.id_servicio_disponibilidad", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "id_agenda",
            "id_servicio_disponibilidad",
            name="uq_detalle"
        ),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    agenda = relationship("Agenda", back_populates="detalles")
    servicio_disponibilidad = relationship("ServicioDisponibilidad", back_populates="detalles")

    def __repr__(self):
        return f"<Detalle id={self.id_detalle} agenda={self.id_agenda}>"
