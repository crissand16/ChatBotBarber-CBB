import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type { Disponibilidad } from '../interfaces/DisponibilidadInter';

export const obtenerDisponibilidadEspecialista = async (
  idEspecialista: string
): Promise<Disponibilidad[]> => {
  const { data } = await api.get<ApiResponse<Disponibilidad[]>>(
    `/disponibilidad/especialista/${idEspecialista}`
  );
  return data.data;
};

export const obtenerDisponibilidadRango = async (
  fechaInicio: string,
  fechaFin: string
): Promise<Disponibilidad[]> => {
  const { data } = await api.get<ApiResponse<Disponibilidad[]>>('/disponibilidad', {
    params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
  });
  return data.data;
};
