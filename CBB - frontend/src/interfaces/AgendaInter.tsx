// Coincide con lo que arma estructurar_agendas() en agenda_controller.py
export interface AgendaServicio {
  id_servicio: number;
  nombre: string;
  precio: number;
}

export interface AgendaPersona {
  id: string;
  nombre: string;
}

export interface Agenda {
  id_agenda: number;
  estado_agenda: string;
  precio_total: number;
  fecha_creacion_agenda: string;
  fecha_agenda: string | null;
  hora_agenda: string | null;
  cliente: AgendaPersona;
  especialista: AgendaPersona;
  servicios: AgendaServicio[];
}

// Body de POST /agendas (app/schema/agenda_schema.py -> AgendaCreate)
export interface AgendaCreate {
  id_cliente: string;
  id_servicio_disponibilidad: number;
  estado_agenda?: string;
}
