export type FiltroRolUsuario = 'todos' | 'cliente' | 'especialista' | 'admin';

// Resultado de una acción sobre una persona (editar, desactivar, reactivar).
export interface MensajeAccion {
  tono: 'exito' | 'error';
  texto: string;
}
