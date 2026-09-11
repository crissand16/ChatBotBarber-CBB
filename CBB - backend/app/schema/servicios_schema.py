from pydantic import BaseModel
from typing import Optional

class ServicioCreate(BaseModel):
    nombre_servicio: str 
    precio_servicio: float 
    duracion_minutos_servicio: int
    descripcion_servicio: str

class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str] = None
    precio_servicio: Optional[float] = None
    duracion_minutos_servicio: Optional[int] = None
    descripcion_servicio: Optional[str] = None