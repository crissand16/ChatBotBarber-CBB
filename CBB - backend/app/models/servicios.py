from sqlalchemy import Column, Integer, String, Numeric
from app.config.database import Base

class Servicios(Base):

    __tablename__ = "servicios"

    id_servicios = Column(
        Integer,
        primary_key=True
    )

    nombre_servicio = Column(
        String(70),
        nullable=False
    )

    precio_servicio = Column(
        Numeric(10, 2),
        nullable=False
    )

    duracion_minutos_servicio = Column(
        Integer,
        nullable=False

    )

    descripcion_servicio = Column(
        String(200),
        nullable=True
    )

   