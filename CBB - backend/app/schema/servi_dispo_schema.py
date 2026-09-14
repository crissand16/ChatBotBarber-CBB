from pydantic import BaseModel

class ServicioDisponibilidadCreate(BaseModel):
    id_servicios: int
    id_disponibilidad: int

class ServicioDisponibilidadOut(ServicioDisponibilidadCreate):
    id_servicio_disponibilidad: int
    id_servicios: int
    id_disponibilidad: int

    class Config:
        from_attributes = True
