export const validarCorreo = (correo: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
};

export const validarPassword = (password: string): boolean => {
  return password.length >= 6;
};

export const validarTelefono = (telefono: string): boolean => {
  return /^[0-9]{7,10}$/.test(telefono);
};