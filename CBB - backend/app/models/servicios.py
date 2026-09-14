from sqlalchemy import Column, Integer, String, Numeric, CheckConstraint
from sqlalchemy.orm import relationship

from app.config.database import Base


class Servicios(Base):

    __tablename__ = "servicios"

    id_servicios = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True)

    nombre_servicio = Column(
        String(70),
        nullable=False)
    precio_servicio = Column(
        Numeric(10, 2),
        nullable=False)
    duracion_minutos_servicio = Column(
        Integer,
        nullable=False, 
        server_default="30")
    descripcion_servicio = Column(
        String(200),
        nullable=True)

    __table_args__ = (
        CheckConstraint("precio_servicio >= 0", 
                        name="chk_servicios_precio"),
        CheckConstraint("duracion_minutos_servicio > 0", 
                        name="chk_servicios_duracion"),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    servicio_disponibilidades = relationship(
        "ServicioDisponibilidad",
        back_populates="servicio",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Servicios id={self.id_servicios} nombre={self.nombre_servicio}>"
