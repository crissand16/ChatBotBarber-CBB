// Coincide con la tabla "usuario" del backend (app/models/usuario.py).
export interface Usuario {
  id_usuario: string;
  nombres_usuario: string;
  apellidos_usuario: string;
  correo_usuario: string;
  fecha_nacimiento_usuario?: string;
  telefono_usuario?: string;
  rol_usuario: 'cliente' | 'especialista' | 'admin';
  fecha_registro_usuario?: string;
}

// Datos que exige POST /usuarios/registro (app/schema/usuario_schema.py -> UsuarioCreate).
export interface UsuarioRegistro {
  id_usuario: string;
  nombres_usuario: string;
  apellidos_usuario: string;
  correo_usuario: string;
  contrasena_usuario: string;
  fecha_nacimiento_usuario: string;
  telefono_usuario: string;
  rol_usuario?: 'cliente' | 'especialista' | 'admin';
}

// Respuesta de POST /usuarios/login.
export interface UsuarioLogin {
  logueado: boolean;
  id_usuario: string;
  nombres: string;
  apellidos: string;
  correo: string;
  rol: string;
}
