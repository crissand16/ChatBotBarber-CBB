import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';

import type { Usuario } from '../interfaces/UsuarioInter';
import type { FiltroRolUsuario } from '../interfaces/EquipoInter';

import {
  obtenerUsuarios,
  obtenerClientes,
  obtenerEspecialistas,
  obtenerAdministradores,
} from '../services/usuarioService';
import { obtenerMensajeError } from '../services/apiError';

import '../App.css';

const FILTROS: { valor: FiltroRolUsuario; etiqueta: string }[] = [
  { valor: 'todos', etiqueta: 'Todos' },
  { valor: 'cliente', etiqueta: 'Clientes' },
  { valor: 'especialista', etiqueta: 'Especialistas' },
  { valor: 'admin', etiqueta: 'Administradores' },
];

const ROL_A_CLASE: Record<string, string> = {
  cliente: 'badge-pendiente',
  especialista: 'badge-confirmada',
  admin: 'badge-cancelada',
};

function Equipo() {
  const [filtro, setFiltro] = useState<FiltroRolUsuario>('todos');
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [cargando, setCargando] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const cargarUsuarios = async () => {
      setCargando(true);
      setError('');

      try {
        let datos: Usuario[] = [];

        if (filtro === 'todos') {
          datos = await obtenerUsuarios();
        } else if (filtro === 'cliente') {
          datos = await obtenerClientes();
        } else if (filtro === 'especialista') {
          datos = await obtenerEspecialistas();
        } else {
          datos = await obtenerAdministradores();
        }

        setUsuarios(datos);
      } catch (err) {
        setUsuarios([]);
        setError(obtenerMensajeError(err, 'No se pudo cargar la lista de personas.'));
      } finally {
        setCargando(false);
      }
    };

    cargarUsuarios();
  }, [filtro]);

  return (
    <Layout>
      <PageHeader
        eyebrow="Panel administrativo"
        title="Equipo y usuarios"
        description="Consulta clientes, especialistas y administradores registrados en el sistema."
      />

      <div className="tabs-filtro">
        {FILTROS.map((opcion) => (
          <button
            type="button"
            key={opcion.valor}
            className={'tab-btn' + (filtro === opcion.valor ? ' activo' : '')}
            onClick={() => setFiltro(opcion.valor)}
          >
            {opcion.etiqueta}
          </button>
        ))}
      </div>

      {cargando && <StatusMessage tono="cargando" titulo="Cargando personas..." />}

      {!cargando && error && <StatusMessage tono="error" titulo={error} />}

      {!cargando && !error && usuarios.length === 0 && (
        <StatusMessage
          tono="vacio"
          titulo="No hay registros para este filtro"
          descripcion="Cuando se registren nuevas personas con este rol, aparecerán aquí."
        />
      )}

      {!cargando && !error && usuarios.length > 0 && (
        <div className="tabla-wrapper">
          <table className="tabla-usuarios">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Teléfono</th>
                <th>Rol</th>
                <th>Registrado</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((usuario) => (
                <tr key={usuario.id_usuario}>
                  <td>
                    {usuario.nombres_usuario} {usuario.apellidos_usuario}
                  </td>
                  <td>{usuario.correo_usuario}</td>
                  <td>{usuario.telefono_usuario ?? '—'}</td>
                  <td>
                    <span className={'badge ' + (ROL_A_CLASE[usuario.rol_usuario] ?? '')}>
                      {usuario.rol_usuario}
                    </span>
                  </td>
                  <td>
                    {usuario.fecha_registro_usuario
                      ? new Date(usuario.fecha_registro_usuario).toLocaleDateString('es-CO')
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}

export default Equipo;
