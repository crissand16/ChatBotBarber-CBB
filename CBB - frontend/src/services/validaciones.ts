import type { PerfilFormState } from '../interfaces/PerfilFormInter';

export const validarCorreo = (correo: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
};

export const validarPassword = (password: string): boolean => {
  return password.length >= 6;
};

export const validarTelefono = (telefono: string): boolean => {
  return /^[0-9]{7,10}$/.test(telefono);
};

// Devuelve el primer error del formulario de perfil, o '' si todo es válido.
// Los límites de longitud coinciden con las columnas del backend (40 caracteres).
export const validarPerfil = (perfil: PerfilFormState): string => {
  const nombres = perfil.nombres_usuario.trim();
  const apellidos = perfil.apellidos_usuario.trim();

  if (nombres.length < 2) return 'El nombre debe tener mínimo 2 caracteres.';
  if (nombres.length > 40) return 'El nombre no puede superar 40 caracteres.';
  if (apellidos.length < 2) return 'El apellido debe tener mínimo 2 caracteres.';
  if (apellidos.length > 40) return 'El apellido no puede superar 40 caracteres.';
  if (!validarCorreo(perfil.correo_usuario.trim())) return 'Ingresa un correo válido.';
  if (!validarTelefono(perfil.telefono_usuario.trim())) {
    return 'El teléfono debe tener entre 7 y 10 dígitos.';
  }
  if (!perfil.fecha_nacimiento_usuario) return 'Selecciona la fecha de nacimiento.';

  return '';
};
