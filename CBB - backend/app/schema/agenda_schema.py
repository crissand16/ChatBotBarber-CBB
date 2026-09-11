from pydantic import BaseModel
from datetime import date
from typing import Optional

class AgendaCreate(BaseModel):
    id_cliente: str
    id_servicio_disponibilidad: int 
    estado_agenda: Optional[str] = 'pendiente'
    fecha_registro_agenda: Optional[date] = None 