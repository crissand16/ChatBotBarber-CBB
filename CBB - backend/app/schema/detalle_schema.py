from pydantic import BaseModel


class DetalleCreate(BaseModel):
    id_agenda: int
    id_servicio_disponibilidad: int


class DetalleOut(BaseModel):
    id_detalle: int
    id_agenda: int
    id_servicio_disponibilidad: int

    class Config:
        from_attributes = True
# Extrae los datos usando los atributos normales de una 
# clase (objeto.atributo)
# en lugar de llaves de diccionario  
