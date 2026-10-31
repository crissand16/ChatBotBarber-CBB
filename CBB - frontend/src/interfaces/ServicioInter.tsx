export interface Servicio {
  id_servicios: number;
  nombre_servicio: string;
  precio_servicio: number;
  duracion_minutos_servicio: number;
  descripcion_servicio?: string | null;
}

// Body de POST /servicios (app/schema/servicio_schema.py -> ServicioCreate)
export interface ServicioCreate {
  nombre_servicio: string;
  precio_servicio: number;
  duracion_minutos_servicio: number;
  descripcion_servicio: string;
}

// Body de PUT /servicios/{id} (app/schema/servicios_schema.py -> ServicioUpdate).
// Solo se modifican los campos que se envían.
export interface ServicioUpdate {
  nombre_servicio?: string;
  precio_servicio?: number;
  duracion_minutos_servicio?: number;
  descripcion_servicio?: string;
}