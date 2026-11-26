from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, datetime


class LoginRequest(BaseModel):

    correo_usuario: str

    contrasena_usuario: str


class UsuarioCreate(BaseModel):
    id_usuario: str = Field(..., min_length=1)
    nombres_usuario: str = Field, field_validator
    apellidos_usuario: str = Field, field_validator
    correo_usuario: EmailStr
    contrasena_usuario: str = Field, field_validator
    fecha_nacimiento_usuario: date
    telefono_usuario: str = Field, field_validator
    rol_usuario: Optional[str] = "cliente"

    @field_validator('contrasena_usuario')
    @classmethod
    def truncar_password(cls, v: str) -> str:
        # Trunca automáticamente la contraseña a 72 caracteres por límite de bcrypt
        return v[:72]


class UsuarioUpdate(BaseModel):
    nombres_usuario: Optional[str] = None
    apellidos_usuario: Optional[str] = None
    correo_usuario: Optional[str] = None
    contrasena_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[date] = None
    telefono_usuario: Optional[str] = None
    rol_usuario: Optional[str] = None


class UsuarioPerfilUpdate(BaseModel):
    """Campos que un especialista o cliente puede editar de su perfil.

    No incluye rol, id ni contraseña: esos cambios no se permiten desde
    el perfil.
    """
    nombres_usuario: Optional[str] = None
    apellidos_usuario: Optional[str] = None
    correo_usuario: Optional[EmailStr] = None
    telefono_usuario: Optional[str] = None
    fecha_nacimiento_usuario: Optional[date] = None


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
