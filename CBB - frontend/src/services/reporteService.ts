import { isAxiosError } from 'axios';
import api from './api';

export type TipoReporte = 'agendas' | 'facturas';
export type FormatoReporte = 'excel' | 'pdf';

// Fechas en formato YYYY-MM-DD. "idEspecialista" solo aplica al reporte de agendas.
export interface FiltrosReporte {
  fechaInicio: string;
  fechaFin: string;
  estado?: string;
  idEspecialista?: string;
}

const EXTENSION: Record<FormatoReporte, string> = {
  excel: 'xlsx',
  pdf: 'pdf',
};

// Con responseType 'blob', Axios entrega los errores del backend (JSON) también como Blob.
// Se convierten a objeto para que obtenerMensajeError pueda leer el campo "mensaje".
const leerErrorDelBlob = async (error: unknown): Promise<void> => {
  if (isAxiosError(error) && error.response?.data instanceof Blob) {
    try {
      const texto = await error.response.data.text();
      (error.response as { data: unknown }).data = JSON.parse(texto);
    } catch {
      // Si no es JSON se deja el error original.
    }
  }
};

export const descargarReporte = async (
  tipo: TipoReporte,
  formato: FormatoReporte,
  filtros: FiltrosReporte
): Promise<void> => {
  try {
    const respuesta = await api.get<Blob>(`/reportes/${tipo}/${formato}`, {
      params: {
        fecha_inicio: filtros.fechaInicio,
        fecha_fin: filtros.fechaFin,
        estado: filtros.estado || undefined,
        id_especialista:
          tipo === 'agendas' ? filtros.idEspecialista || undefined : undefined,
      },
      responseType: 'blob',
    });

    const url = URL.createObjectURL(respuesta.data);
    const enlace = document.createElement('a');
    enlace.href = url;
    enlace.download = `reporte_${tipo}_${filtros.fechaInicio}_${filtros.fechaFin}.${EXTENSION[formato]}`;
    document.body.appendChild(enlace);
    enlace.click();
    enlace.remove();
    URL.revokeObjectURL(url);
  } catch (error) {
    await leerErrorDelBlob(error);
    throw error;
  }
};