// Coincide con la tabla intermedia "servicio_disponibilidad"
// (app/models/servicio_disponibilidad.py y servi_dispo_controller.py).
// Une un servicio puntual con un horario disponible de un especialista.
export interface ServicioDisponibilidad {
  id_servicio_disponibilidad: number;
  id_servicios: number;
  id_disponibilidad: number;
}

// Body de POST /servicio_disponibilidad
export interface ServicioDisponibilidadCreate {
  id_servicios: number;
  id_disponibilidad: number;
}
