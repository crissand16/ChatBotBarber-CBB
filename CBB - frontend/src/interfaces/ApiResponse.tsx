// Estructura fija que devuelve el backend en TODAS las respuestas
// (ver app/utils/response.py -> response_success / response_error).
export interface ApiResponse<T> {
  status: boolean;
  mensaje: string;
  data: T;
  error: string | null;
  code: number;
}
