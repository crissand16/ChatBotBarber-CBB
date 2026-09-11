from pydantic import BaseModel

class DetalleCreate(BaseModel):
    id_agenda: int
    id_servicio_disponibilidad: int 