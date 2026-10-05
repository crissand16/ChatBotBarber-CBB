from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
# Field función de Pydantic para añadir restricciones a un atributo
#... campo obligatorio -- ge mayor o igual que


class FacturaCreate(BaseModel):
    id_agenda: int
    subtotal_factura: float = Field(..., ge=0)
    iva_factura: float = Field(..., ge=0)
    total_factura: float = Field(..., ge=0)
    metodo_pago_factura: Optional[str] = Field(
        default="efectivo",
        description="Valores permitidos: efectivo, transferencia"
    )


class FacturaUpdateEstado(BaseModel):
    nuevo_estado: str = Field(
        ...,
        example="pagada",
        description="Estados permitidos: pendiente, pagada"
    )


class FacturaOut(BaseModel):
    id_factura: int
    id_agenda: int
    fecha_factura: datetime
    subtotal_factura: float
    iva_factura: float
    total_factura: float
    estado_factura: str
    metodo_pago_factura: str

    class Config:
        from_attributes = True
