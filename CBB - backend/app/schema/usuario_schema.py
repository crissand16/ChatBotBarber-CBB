from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

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

class UsuarioUpdate(BaseModel):
    nombres_usuario: Optional[str] = None
    apellidos_usuario: Optional[str] = None
    correo_usuario: Optional[str] = None
    contrasena_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[date] = None
    telefono_usuario: Optional[str] = None
    rol_usuario: Optional[str] = None

class UsuarioOut(BaseModel):
    id_usuario: str
    nombres_usuario: str
    apellidos_usuario: str
    correo_usuario: EmailStr
    fecha_nacimiento_usuario: date
    telefono_usuario: str
    rol_usuario: str
    fecha_registro_usuario: datetime

    class Config:
        from_attributes = True