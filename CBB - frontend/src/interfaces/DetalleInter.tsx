// Coincide con la tabla "detalle" (app/models/detalle.py y
// detalle_controller.py). Relaciona una agenda con el
// servicio_disponibilidad que la compone. El backend ya crea este
// registro automáticamente al agendar una cita (POST /agendas), por
// lo que estos endpoints quedan disponibles para consultas puntuales
// o soporte administrativo.
export interface Detalle {
  id_detalle: number;
  id_agenda: number;
  id_servicio_disponibilidad: number;
}

// Body de POST /detalle
export interface DetalleCreate {
  id_agenda: number;
  id_servicio_disponibilidad: number;
}
