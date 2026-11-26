export type StatusMessageTono = 'cargando' | 'error' | 'vacio' | 'exito';

export interface StatusMessageProps {
  tono: StatusMessageTono;
  titulo: string;
  descripcion?: string;
}
