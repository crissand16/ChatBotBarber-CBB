from datetime import date, time
from typing import Optional

from pydantic import BaseModel, model_validator


class DisponibilidadCreate(BaseModel):
    id_especialista: str
    fecha_disponibilidad: date
    hora_inicio_disponibilidad: time
    hora_fin_disponibilidad: time
    estado_disponibilidad: Optional[str] = "disponible"

    @model_validator(mode="after")
    def validar_horas(self):
        if self.hora_fin_disponibilidad <= self.hora_inicio_disponibilidad:
            raise ValueError(
                "hora_fin_disponibilidad debe ser mayor que hora_inicio_disponibilidad"
            )
        return self


class DisponibilidadUpdate(BaseModel):
    fecha_disponibilidad: Optional[date] = None
    hora_inicio_disponibilidad: Optional[time] = None
    hora_fin_disponibilidad: Optional[time] = None
    estado_disponibilidad: Optional[str] = None


class DisponibilidadOut(BaseModel):
    id_disponibilidad: int
    id_especialista: str
    fecha_disponibilidad: date
    hora_inicio_disponibilidad: time
    hora_fin_disponibilidad: time
    estado_disponibilidad: str

    class Config:
        from_attributes = True
