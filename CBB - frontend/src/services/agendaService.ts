import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type { Agenda, AgendaCreate, EstadoAgenda } from '../interfaces/AgendaInter';

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

// Usado por especialista/administrador para aceptar, rechazar, completar
// o cancelar una cita (PATCH /agendas/{id_agenda}/estado).
export const cambiarEstadoAgenda = async (
  idAgenda: number,
  nuevoEstado: EstadoAgenda
): Promise<{ id_agenda: number; estado_agenda: string }> => {
  const { data } = await api.patch<ApiResponse<{ id_agenda: number; estado_agenda: string }>>(
    `/agendas/${idAgenda}/estado`,
    { nuevo_estado: nuevoEstado }
  );
  return data.data;
};

// Cancela una cita (el cliente cancela su propia cita). El backend libera
// la disponibilidad asociada automáticamente.
export const anularAgenda = async (idAgenda: number): Promise<void> => {
  await api.delete<ApiResponse<null>>(`/agendas/${idAgenda}`);
};
