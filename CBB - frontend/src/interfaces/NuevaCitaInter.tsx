import type { Disponibilidad } from './DisponibilidadInter';

// Franja de disponibilidad ya cruzada con el servicio_disponibilidad
// que la habilita para el servicio elegido, lista para reservarse.
export interface FranjaReservable extends Disponibilidad {
  id_servicio_disponibilidad: number;
}

export type PasoReserva = 1 | 2 | 3;
