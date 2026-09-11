import api from './api';
import type { ApiResponse } from '../interfaces/ApiResponse';
import type {
  Usuario,
  UsuarioRegistro,
  UsuarioLogin,
} from '../interfaces/UsuarioInter';

export const obtenerUsuarios = async (): Promise<Usuario[]> => {
  const { data } = await api.get<ApiResponse<Usuario[]>>('/usuarios');
  return data.data;
};

export const obtenerClientes = async (): Promise<Usuario[]> => {
  const { data } = await api.get<ApiResponse<Usuario[]>>('/usuarios/clientes');
  return data.data;
};

export const obtenerEspecialistas = async (): Promise<Usuario[]> => {
  const { data } = await api.get<ApiResponse<Usuario[]>>('/usuarios/especialistas');
  return data.data;
};

export const obtenerAdministradores = async (): Promise<Usuario[]> => {
  const { data } = await api.get<ApiResponse<Usuario[]>>('/usuarios/administradores');
  return data.data;
};

export const obtenerUsuarioPorId = async (
  idUsuario: string
): Promise<Usuario> => {
  const { data } = await api.get<ApiResponse<Usuario>>(`/usuarios/${idUsuario}`);
  return data.data;
};

export const registrarUsuario = async (
  datos: UsuarioRegistro
): Promise<Usuario> => {
  const { data } = await api.post<ApiResponse<Usuario>>('/usuarios/registro', datos);
  return data.data;
};

export const loginUsuario = async (
  correo_usuario: string,
  contrasena_usuario: string
): Promise<UsuarioLogin> => {
  const { data } = await api.post<ApiResponse<UsuarioLogin>>('/usuarios/login', {
    correo_usuario,
    contrasena_usuario,
  });
  return data.data;
};
