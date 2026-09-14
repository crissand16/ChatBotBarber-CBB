from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class ServicioDisponibilidad(Base):
    """
    Tabla intermedia que asocia un servicio concreto con un
    bloque de disponibilidad de un especialista.
    """

    __tablename__ = "servicio_disponibilidad"

    id_servicio_disponibilidad = Column(Integer, primary_key=True, autoincrement=True)

    id_servicios = Column(
        Integer,
        ForeignKey("servicios.id_servicios", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    id_disponibilidad = Column(
        Integer,
        ForeignKey("disponibilidad.id_disponibilidad", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "id_servicios",
            "id_disponibilidad",
            name="uq_servicio_disponibilidad"
        ),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    servicio = relationship("Servicios", back_populates="servicio_disponibilidades")
    disponibilidad = relationship("Disponibilidad", back_populates="servicio_disponibilidades")

    detalles = relationship(
        "Detalle",
        back_populates="servicio_disponibilidad",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ServicioDisponibilidad id={self.id_servicio_disponibilidad}>"
