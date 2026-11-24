import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type { Pqr, PqrCreate } from '../interfaces/PqrInter';

// Radica una petición, queja o reclamo. El backend la guarda y la envía
// por correo al administrador (que responde desde su Gmail).
export const enviarPqr = async (datos: PqrCreate): Promise<Pqr> => {
  const { data } = await api.post<ApiResponse<Pqr>>('/pqr', datos);
  return data.data;
};
