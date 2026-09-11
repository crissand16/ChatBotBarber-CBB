from pydantic import BaseModel

class ServicioDisponibilidadCreate(BaseModel):
    id_servicios: int 
    id_disponibilidad: int 