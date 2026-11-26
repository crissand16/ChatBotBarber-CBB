// Tipos de solicitud del buzón (app/schema/pqr_schema.py -> TipoPqr).
export type TipoPqr = 'peticion' | 'queja' | 'reclamo';

// Body de POST /pqr (app/schema/pqr_schema.py -> PqrCreate).
export interface PqrCreate {
  id_usuario: string;
  nombre: string;
  correo: string;
  tipo: TipoPqr;
  asunto: string;
  mensaje: string;
}

// Respuesta de POST /pqr (app/schema/pqr_schema.py -> PqrOut).
export interface Pqr {
  id_pqr: number;
  radicado: string;
  id_usuario: string;
  nombre_pqr: string;
  correo_pqr: string;
  tipo_pqr: TipoPqr;
  asunto_pqr: string;
  mensaje_pqr: string;
  estado_pqr: string;
  correo_enviado_pqr: boolean;
  fecha_creacion_pqr: string;
}
