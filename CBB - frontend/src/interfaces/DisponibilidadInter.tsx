// Fila devuelta por obtener_disponibilidad_especialista / obtener_disponibilidad_rango
export interface Disponibilidad {
  id_disponibilidad: number;
  id_especialista: string;
  nombres_usuario: string;
  apellidos_usuario: string;
  fecha_disponibilidad: string;
  hora_inicio_disponibilidad: string;
  hora_fin_disponibilidad: string;
  estado_disponibilidad: 'disponible' | 'ocupado' | string;
}
