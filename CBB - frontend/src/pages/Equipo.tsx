import { useCallback, useEffect, useState } from 'react';
import type {FormEvent} from 'react';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type { Usuario } from '../interfaces/UsuarioInter';
import type { FiltroRolUsuario, MensajeAccion } from '../interfaces/EquipoInter';
import type { PerfilFormState } from '../interfaces/PerfilFormInter';


import {
  obtenerUsuarios,
  obtenerClientes,
  obtenerEspecialistas,
  obtenerAdministradores,
  editarEspecialista,
  desactivarEspecialista,
} from '../services/usuarioService';
import { obtenerMensajeError } from '../services/apiError';
import { validarPerfil } from '../services/validaciones';
import {
  FORMULARIO_PERFIL_VACIO,
  aFormularioPerfil,
  aPayloadPerfil,
} from '../interfaces/perfilForm';

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

  const [editando, setEditando] = useState<Usuario | null>(null);
  const [formulario, setFormulario] = useState<PerfilFormState>(FORMULARIO_PERFIL_VACIO);
  const [errorFormulario, setErrorFormulario] = useState<string>('');
  const [guardando, setGuardando] = useState<boolean>(false);

  const [mensaje, setMensaje] = useState<MensajeAccion | null>(null);
  const [procesandoId, setProcesandoId] = useState<string | null>(null);


    const cargarUsuarios = useCallback(async () => {
    setCargando(true);
    setError('');

    try {
      let datos: Usuario[] = [];

      if (filtro === 'todos') {
        datos = await obtenerUsuarios();
      } else if (filtro === 'cliente') {
        datos = await obtenerClientes();
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
  }, [filtro]);

  useEffect(() => {
    cargarUsuarios();
  }, [cargarUsuarios]);

  const iniciarEdicion = (usuario: Usuario) => {
    setEditando(usuario);
    setFormulario(aFormularioPerfil(usuario));
    setErrorFormulario('');
    setMensaje(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const cancelarEdicion = () => {
    setEditando(null);
    setFormulario(FORMULARIO_PERFIL_VACIO);
    setErrorFormulario('');
  };

  const manejarCambio = (campo: keyof PerfilFormState, valor: string) => {
    setFormulario({ ...formulario, [campo]: valor });
  };

  const manejarGuardar = async (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    if (!editando) return;

    setErrorFormulario('');

    const mensajeValidacion = validarPerfil(formulario);
    if (mensajeValidacion) {
      setErrorFormulario(mensajeValidacion);
      return;
    }

    setGuardando(true);
    try {
      await editarEspecialista(editando.id_usuario, aPayloadPerfil(formulario));
      cancelarEdicion();
      setMensaje({ tono: 'exito', texto: 'Especialista actualizado correctamente.' });
      await cargarUsuarios();
    } catch (err) {
      setErrorFormulario(obtenerMensajeError(err, 'No se pudo actualizar el especialista.'));
    } finally {
      setGuardando(false);
    }
  };

  const manejarDesactivar = async (usuario: Usuario) => {
    const nombre = `${usuario.nombres_usuario} ${usuario.apellidos_usuario}`;
    const confirmado = window.confirm(
      `¿Desactivar a ${nombre}? No podrá iniciar sesión ni recibir nuevas citas.`
    );
    if (!confirmado) return;

    setProcesandoId(usuario.id_usuario);
    setMensaje(null);

    try {
      await desactivarEspecialista(usuario.id_usuario);
      setMensaje({ tono: 'exito', texto: `${nombre} fue desactivado.` });
      await cargarUsuarios();
    } catch (err) {
      setMensaje({
        tono: 'error',
        texto: obtenerMensajeError(err, 'No se pudo desactivar al especialista.'),
      });
    } finally {
      setProcesandoId(null);
    }
  };


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

      {editando && (
        <form className="panel-form" onSubmit={manejarGuardar}>
          <h3 className="panel-form-titulo">
            Editar especialista: {editando.nombres_usuario} {editando.apellidos_usuario}
          </h3>

          <div className="panel-form-grid">
            <div className="form-group">
              <label htmlFor="esp_nombres">Nombres</label>
              <input
                id="esp_nombres"
                value={formulario.nombres_usuario}
                onChange={(e) => manejarCambio('nombres_usuario', e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="esp_apellidos">Apellidos</label>
              <input
                id="esp_apellidos"
                value={formulario.apellidos_usuario}
                onChange={(e) => manejarCambio('apellidos_usuario', e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="esp_correo">Correo</label>
              <input
                id="esp_correo"
                type="email"
                value={formulario.correo_usuario}
                onChange={(e) => manejarCambio('correo_usuario', e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="esp_telefono">Teléfono</label>
              <input
                id="esp_telefono"
                value={formulario.telefono_usuario}
                onChange={(e) => manejarCambio('telefono_usuario', e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="esp_nacimiento">Fecha de nacimiento</label>
              <input
                id="esp_nacimiento"
                type="date"
                value={formulario.fecha_nacimiento_usuario}
                onChange={(e) => manejarCambio('fecha_nacimiento_usuario', e.target.value)}
              />
            </div>
          </div>

          {errorFormulario && <p className="form-error">{errorFormulario}</p>}

          <div className="panel-form-acciones">
            <Button type="submit" variant="success" disabled={guardando}>
              {guardando ? 'Guardando...' : 'Guardar cambios'}
            </Button>
            <Button variant="outline" onClick={cancelarEdicion} disabled={guardando}>
              Cancelar
            </Button>
          </div>
        </form>
      )}

      {mensaje && <StatusMessage tono={mensaje.tono} titulo={mensaje.texto} />}


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
                  <td>
                    {usuario.rol_usuario === 'especialista' ? (
                      <div className="acciones-fila">
                        <Button
                          variant="outline"
                          onClick={() => iniciarEdicion(usuario)}
                          disabled={procesandoId === usuario.id_usuario}
                        >
                          Editar
                        </Button>
                        (
                          <Button
                            variant="danger"
                            onClick={() => manejarDesactivar(usuario)}
                            disabled={procesandoId === usuario.id_usuario}
                          >
                            Desactivar
                          </Button>
                        ) 
                      </div>
                    ) : (
                      '—'
                    )}
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
