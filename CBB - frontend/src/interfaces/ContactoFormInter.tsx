import type { TipoPqr } from './PqrInter';

// Estado del formulario del buzón PQR (Contacto/buzón).
export interface ContactoFormState {
  nombre: string;
  correo: string;
  tipo: TipoPqr;
  asunto: string;
  mensaje: string;
}

export interface ContactoInfoItem {
  icono: string;
  titulo: string;
  valor: string;
  href?: string;
}

// Opción del selector Petición / Queja / Reclamo.
export interface PqrTipoOpcion {
  valor: TipoPqr;
  icono: string;
  titulo: string;
  descripcion: string;
}
