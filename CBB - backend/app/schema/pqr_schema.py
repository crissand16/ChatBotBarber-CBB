from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

TipoPqr = Literal["peticion", "queja", "reclamo"]


class PqrCreate(BaseModel):
    # Quita espacios al inicio/fin antes de validar la longitud
    model_config = ConfigDict(str_strip_whitespace=True)

    id_usuario: str
    nombre: str = Field(min_length=3, max_length=100)
    correo: EmailStr
    tipo: TipoPqr
    asunto: str = Field(min_length=5, max_length=120)
    mensaje: str = Field(min_length=10, max_length=2000)

    @field_validator("correo")
    @classmethod
    def correo_maximo_60(cls, valor):
        # Misma longitud que usuario.correo_usuario
        if len(valor) > 60:
            raise ValueError("El correo no puede superar 60 caracteres")
        return valor


class PqrOut(BaseModel):
    id_pqr: int
    radicado: str
    id_usuario: str
    nombre_pqr: str
    correo_pqr: str
    tipo_pqr: str
    asunto_pqr: str
    mensaje_pqr: str
    estado_pqr: str
    correo_enviado_pqr: bool
    fecha_creacion_pqr: datetime

    model_config = ConfigDict(from_attributes=True)
