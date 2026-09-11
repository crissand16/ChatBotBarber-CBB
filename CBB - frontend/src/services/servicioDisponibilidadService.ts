import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type {
  ServicioDisponibilidad,
  ServicioDisponibilidadCreate,
} from '../interfaces/ServicioDisponibilidadInter';

// Lista todas las combinaciones servicio + disponibilidad registradas.
// Se usa para saber, dado un servicio, qué franjas de disponibilidad
// (id_disponibilidad) están habilitadas para agendarse.
export const obtenerServicioDisponibilidad = async (): Promise<
  ServicioDisponibilidad[]
> => {
  const { data } = await api.get<ApiResponse<ServicioDisponibilidad[]>>(
    '/servicio_disponibilidad'
  );
  return data.data;
};

export const obtenerServicioDisponibilidadPorId = async (
  id: number
): Promise<ServicioDisponibilidad> => {
  const { data } = await api.get<ApiResponse<ServicioDisponibilidad>>(
    `/servicio_disponibilidad/${id}`
  );
  return data.data;
};

export const crearServicioDisponibilidad = async (
  datos: ServicioDisponibilidadCreate
): Promise<ServicioDisponibilidad> => {
  const { data } = await api.post<ApiResponse<ServicioDisponibilidad>>(
    '/servicio_disponibilidad',
    datos
  );
  return data.data;
};
