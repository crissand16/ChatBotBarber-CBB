import type { PerfilFormState } from '../interfaces/PerfilFormInter';
import type { ContactoFormState } from '../interfaces/ContactoFormInter';

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

// Devuelve el primer error del formulario del buzón PQR, o '' si todo es válido.
// Los límites coinciden con PqrCreate en el backend.
export const validarPqr = (pqr: ContactoFormState): string => {
  const nombre = pqr.nombre.trim();
  const correo = pqr.correo.trim();
  const asunto = pqr.asunto.trim();
  const mensaje = pqr.mensaje.trim();

  if (nombre.length < 3) return 'Ingresa tu nombre completo.';
  if (nombre.length > 100) return 'El nombre no puede superar 100 caracteres.';
  if (!validarCorreo(correo)) return 'Ingresa un correo electrónico válido.';
  if (correo.length > 60) return 'El correo no puede superar 60 caracteres.';
  if (asunto.length < 5) return 'Escribe un asunto de mínimo 5 caracteres.';
  if (asunto.length > 120) return 'El asunto no puede superar 120 caracteres.';
  if (mensaje.length < 10) return 'Cuéntanos un poco más: mínimo 10 caracteres.';
  if (mensaje.length > 2000) return 'El mensaje no puede superar 2000 caracteres.';

  return '';
};
