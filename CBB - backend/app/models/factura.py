from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class Factura(Base):

    __tablename__ = "factura"

    id_factura = Column(Integer, primary_key=True, autoincrement=True)

    fecha_factura = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    subtotal_factura = Column(
        Numeric(10, 2), 
        nullable=False)
    
    iva_factura = Column(
        Numeric(10, 2), 
        nullable=False)
    
    total_factura = Column(
        Numeric(10, 2), 
        nullable=False)

    estado_factura = Column(
        String(20), 
        nullable=False, 
        server_default="pendiente")
    
    metodo_pago_factura = Column(
        String(20), 
        nullable=False, 
        server_default="efectivo")

    id_agenda = Column(
        Integer,
        ForeignKey("agenda.id_agenda", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        unique=True
    )

    __table_args__ = (
        CheckConstraint("subtotal_factura >= 0", 
                        name="chk_factura_subtotal"),
        CheckConstraint("iva_factura >= 0", 
                        name="chk_factura_iva"),
        CheckConstraint("total_factura >= 0", 
                        name="chk_factura_total"),
        CheckConstraint(
            "estado_factura IN ('pendiente', 'pagada')",
            name="chk_factura_estado"),
        CheckConstraint(
            "metodo_pago_factura IN ('efectivo', 'transferencia')",
            name="chk_factura_metodo_pago"),
    )

    # =========================================================
    # RELACIONES
    # =========================================================

    agenda = relationship("Agenda", back_populates="factura")

    def __repr__(self):
        return f"<Factura id={self.id_factura} estado={self.estado_factura}>"
