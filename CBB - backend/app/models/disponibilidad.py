from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Disponibilidad(Base):

    __tablename__ = "disponibilidad"

    id_disponibilidad = Column(Integer, primary_key=True, autoincrement=True)
    id_especialista = Column(
        String(10),
        ForeignKey("usuario.id_usuario", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    fecha_disponibilidad = Column(Date, nullable=False)
    hora_inicio_disponibilidad = Column(Time, nullable=False)
    hora_fin_disponibilidad = Column(Time, nullable=False)

    estado_disponibilidad = Column(String(20), nullable=False, server_default="ocupado")

    __table_args__ = (
        CheckConstraint(
            "estado_disponibilidad IN ('disponible', 'ocupado')",
            name="chk_disponibilidad_estado"
        ),
        UniqueConstraint(
            "id_especialista",
            "fecha_disponibilidad",
            "hora_inicio_disponibilidad",
            name="uq_dispobilidad_especialista_fecha_hora"
        ),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    especialista = relationship(
        "Usuario",
        back_populates="disponibilidades",
        foreign_keys=[id_especialista]
    )

    servicio_disponibilidades = relationship(
        "ServicioDisponibilidad",
        back_populates="disponibilidad",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Disponibilidad id={self.id_disponibilidad} estado={self.estado_disponibilidad}>"
