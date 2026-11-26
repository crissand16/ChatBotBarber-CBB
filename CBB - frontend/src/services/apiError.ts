import { AxiosError } from 'axios';
import type { ApiResponse } from '../interfaces/ApiResponse';

// El backend siempre responde con { mensaje, error, ... } incluso en
// los errores (400/401/404/500), así que preferimos ese mensaje antes
// de caer en uno genérico.
export const obtenerMensajeError = (
  error: unknown,
  fallback = 'Ocurrió un error inesperado. Intenta nuevamente.'
): string => {
  if (error instanceof AxiosError) {
    const respuesta = error.response?.data as ApiResponse<unknown> | undefined;

    if (respuesta?.mensaje) {
      // Si el backend trae además un detalle técnico distinto al
      // mensaje (por ejemplo "error": "IntegrityError: ..."), lo
      // agregamos para no perder información útil al depurar.
      const detalle =
        typeof respuesta.error === 'string' &&
        respuesta.error.trim() &&
        respuesta.error !== respuesta.mensaje
          ? ` (${respuesta.error})`
          : '';
      return respuesta.mensaje + detalle;
    }
    if (error.code === 'ERR_NETWORK') {
      return 'No se pudo conectar con el servidor. Verifica que el backend esté encendido.';
    }
  }
  return fallback;
};
