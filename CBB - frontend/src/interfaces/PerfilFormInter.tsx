// Estado local de los formularios de perfil (Perfil.tsx y edición de
// especialistas en Equipo.tsx). Todos los campos son texto porque vienen de un <input>.
export interface PerfilFormState {
  nombres_usuario: string;
  apellidos_usuario: string;
  correo_usuario: string;
  telefono_usuario: string;
  fecha_nacimiento_usuario: string;
}
