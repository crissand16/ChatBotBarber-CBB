from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class LoginRequest(BaseModel):

    correo_usuario: str

    contrasena_usuario: str

class UsuarioCreate(BaseModel):
    id_usuario: str
    nombres_usuario: str
    apellidos_usuario: str
    correo_usuario: EmailStr
    contrasena_usuario: str
    fecha_nacimiento_usuario: date 
    telefono_usuario: str
    rol_usuario: Optional[str] = "cliente"