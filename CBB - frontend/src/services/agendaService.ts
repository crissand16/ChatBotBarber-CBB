import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type { Agenda, AgendaCreate } from '../interfaces/AgendaInter';

export const crearAgenda = async (datos: AgendaCreate): Promise<Agenda> => {
  const { data } = await api.post<ApiResponse<Agenda>>('/agendas', datos);
  return data.data;
};

export const obtenerAgendasPorCliente = async (
  idCliente: string
): Promise<Agenda[]> => {
  const { data } = await api.get<ApiResponse<Agenda[]>>(
    `/agendas/cliente/${idCliente}`
  );
  return data.data;
};

export const obtenerAgendasPorEspecialista = async (
  idEspecialista: string
): Promise<Agenda[]> => {
  const { data } = await api.get<ApiResponse<Agenda[]>>(
    `/agendas/especialista/${idEspecialista}`
  );
  return data.data;
};

export const obtenerAgendasPorFecha = async (
  fecha: string
): Promise<Agenda[]> => {
  const { data } = await api.get<ApiResponse<Agenda[]>>(`/agendas/fecha/${fecha}`);
  return data.data;
};
