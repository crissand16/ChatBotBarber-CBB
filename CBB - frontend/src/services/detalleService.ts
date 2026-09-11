import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type { Detalle, DetalleCreate } from '../interfaces/DetalleInter';

// El backend crea el detalle de una agenda automáticamente al
// llamar POST /agendas, así que normalmente no hace falta usar estos
// métodos desde el flujo de reserva. Se exponen para soporte y
// auditoría (por ejemplo, revisar qué servicio_disponibilidad quedó
// asociado a una agenda puntual).
export const obtenerDetalles = async (): Promise<Detalle[]> => {
  const { data } = await api.get<ApiResponse<Detalle[]>>('/detalle');
  return data.data;
};

export const obtenerDetallePorId = async (id: number): Promise<Detalle> => {
  const { data } = await api.get<ApiResponse<Detalle>>(`/detalle/${id}`);
  return data.data;
};

export const crearDetalle = async (
  datos: DetalleCreate
): Promise<Detalle> => {
  const { data } = await api.post<ApiResponse<Detalle>>('/detalle', datos);
  return data.data;
};
