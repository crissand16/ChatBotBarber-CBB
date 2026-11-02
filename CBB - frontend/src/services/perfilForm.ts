import type { PerfilFormState } from '../interfaces/PerfilFormInter';
import type { Usuario, UsuarioPerfilUpdate } from '../interfaces/UsuarioInter';

export const FORMULARIO_PERFIL_VACIO: PerfilFormState = {
  nombres_usuario: '',
  apellidos_usuario: '',
  correo_usuario: '',
  telefono_usuario: '',
  fecha_nacimiento_usuario: '',
};

// De los datos del backend al estado del formulario.
export const aFormularioPerfil = (usuario: Usuario): PerfilFormState => ({
  nombres_usuario: usuario.nombres_usuario,
  apellidos_usuario: usuario.apellidos_usuario,
  correo_usuario: usuario.correo_usuario,
  telefono_usuario: usuario.telefono_usuario ?? '',
  fecha_nacimiento_usuario: usuario.fecha_nacimiento_usuario ?? '',
});

// Del estado del formulario al body que espera el backend (UsuarioPerfilUpdate).
export const aPayloadPerfil = (formulario: PerfilFormState): UsuarioPerfilUpdate => ({
  nombres_usuario: formulario.nombres_usuario.trim(),
  apellidos_usuario: formulario.apellidos_usuario.trim(),
  correo_usuario: formulario.correo_usuario.trim(),
  telefono_usuario: formulario.telefono_usuario.trim(),
  fecha_nacimiento_usuario: formulario.fecha_nacimiento_usuario,
});
