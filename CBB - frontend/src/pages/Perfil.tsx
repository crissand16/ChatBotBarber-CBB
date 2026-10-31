import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import { useAuth } from '../context/AuthContext';

import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type {PerfilFormState,} from '../interfaces/PerfilFormInter';

import {obtenerUsuarioPorId,editarPerfilCliente,editarEspecialista,} from '../services/usuarioService';

import { obtenerMensajeError } from '../services/apiError';
import { validarPerfil } from '../services/validaciones';

import {
  FORMULARIO_PERFIL_VACIO,
  aFormularioPerfil,
  aPayloadPerfil,
} from '../interfaces/perfilForm';


import '../App.css';

const ROL_ETIQUETA: Record<string, string> = {
  cliente: 'Cliente',
  especialista: 'Especialista',
  admin: 'Administrador',
};

function Perfil() {
  const { usuario, iniciarSesion } = useAuth();

  const idUsuario = usuario?.id_usuario;
  // El backend solo expone edición de perfil para clientes y especialistas.
  const puedeEditarPerfil = usuario?.rol === 'cliente' || usuario?.rol === 'especialista';

  const [formulario, setFormulario] = useState<PerfilFormState>(FORMULARIO_PERFIL_VACIO);
  const [cargandoPerfil, setCargandoPerfil] = useState<boolean>(false);
  const [guardandoPerfil, setGuardandoPerfil] = useState<boolean>(false);
  const [errorPerfil, setErrorPerfil] = useState<string>('');
  const [exitoPerfil, setExitoPerfil] = useState<string>('');


  useEffect(() => {
    if (!idUsuario || !puedeEditarPerfil) return;

    const cargarPerfil = async () => {
      setCargandoPerfil(true);
      setErrorPerfil('');

      try {
        const datos = await obtenerUsuarioPorId(idUsuario);
        setFormulario(aFormularioPerfil(datos));
      } catch (err) {
        setErrorPerfil(obtenerMensajeError(err, 'No se pudieron cargar tus datos.'));
      } finally {
        setCargandoPerfil(false);
      }
    };

    cargarPerfil();
  }, [idUsuario, puedeEditarPerfil]);

  const manejarCambioPerfil = (campo: keyof PerfilFormState, valor: string) => {
    setFormulario({ ...formulario, [campo]: valor });
  };

  const manejarGuardarPerfil = async (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    if (!usuario) return;

    setErrorPerfil('');
    setExitoPerfil('');

    const mensajeValidacion = validarPerfil(formulario);
    if (mensajeValidacion) {
      setErrorPerfil(mensajeValidacion);
      return;
    }

    setGuardandoPerfil(true);
    try {
      const payload = aPayloadPerfil(formulario);
      const actualizado =
        usuario.rol === 'cliente'
          ? await editarPerfilCliente(usuario.id_usuario, payload)
          : await editarEspecialista(usuario.id_usuario, payload);

      // Se actualiza la sesión para que el menú lateral muestre el nombre nuevo.
      iniciarSesion({
        ...usuario,
        nombres: actualizado.nombres_usuario,
        apellidos: actualizado.apellidos_usuario,
        correo: actualizado.correo_usuario,
      });
      setFormulario(aFormularioPerfil(actualizado));
      setExitoPerfil('Tus datos se actualizaron correctamente.');
    } catch (err) {
      setErrorPerfil(obtenerMensajeError(err, 'No se pudo actualizar tu perfil.'));
    } finally {
      setGuardandoPerfil(false);
    }
  };


  const iniciales = usuario
    ? `${usuario.nombres.charAt(0)}${usuario.apellidos.charAt(0)}`.toUpperCase()
    : '';

  return (
    <Layout>
      <PageHeader
        eyebrow="Tu cuenta"
        title="Mi perfil"
        description="Consulta y actualiza la información asociada a tu cuenta de ChatBotBarber."
      />

      {usuario && (
        <div className="perfil-card">
          <div className="perfil-avatar">{iniciales}</div>

          <div className="perfil-datos">
            <h2>
              {usuario.nombres} {usuario.apellidos}
            </h2>
            <span className="badge badge-confirmada">
              {ROL_ETIQUETA[usuario.rol] ?? usuario.rol}
            </span>

            <dl className="perfil-lista">
              <div>
                <dt>Correo</dt>
                <dd>{usuario.correo}</dd>
              </div>
              <div>
                <dt>Identificador</dt>
                <dd>{usuario.id_usuario}</dd>
              </div>
            </dl>
          </div>
        </div>
      )}

      {usuario && (
        <div className="perfil-secciones">
          {puedeEditarPerfil && (
            <form className="panel-form" onSubmit={manejarGuardarPerfil}>
              <h3 className="panel-form-titulo">Editar mis datos</h3>

              {cargandoPerfil && (
                <StatusMessage tono="cargando" titulo="Cargando tus datos..." />
              )}

              {!cargandoPerfil && (
                <>
                  <div className="panel-form-grid">
                    <div className="form-group">
                      <label htmlFor="perfil_nombres">Nombres</label>
                      <input
                        id="perfil_nombres"
                        value={formulario.nombres_usuario}
                        onChange={(e) => manejarCambioPerfil('nombres_usuario', e.target.value)}
                        autoComplete="given-name"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="perfil_apellidos">Apellidos</label>
                      <input
                        id="perfil_apellidos"
                        value={formulario.apellidos_usuario}
                        onChange={(e) => manejarCambioPerfil('apellidos_usuario', e.target.value)}
                        autoComplete="family-name"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="perfil_correo">Correo</label>
                      <input
                        id="perfil_correo"
                        type="email"
                        value={formulario.correo_usuario}
                        onChange={(e) => manejarCambioPerfil('correo_usuario', e.target.value)}
                        autoComplete="email"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="perfil_telefono">Teléfono</label>
                      <input
                        id="perfil_telefono"
                        value={formulario.telefono_usuario}
                        onChange={(e) => manejarCambioPerfil('telefono_usuario', e.target.value)}
                        autoComplete="tel"
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="perfil_nacimiento">Fecha de nacimiento</label>
                      <input
                        id="perfil_nacimiento"
                        type="date"
                        value={formulario.fecha_nacimiento_usuario}
                        onChange={(e) =>
                          manejarCambioPerfil('fecha_nacimiento_usuario', e.target.value)
                        }
                      />
                    </div>
                  </div>

                  {errorPerfil && <p className="form-error">{errorPerfil}</p>}
                  {exitoPerfil && <StatusMessage tono="exito" titulo={exitoPerfil} />}

                  <Button type="submit" variant="success" disabled={guardandoPerfil}>
                    {guardandoPerfil ? 'Guardando...' : 'Guardar cambios'}
                  </Button>
                </>
              )}
            </form>
          )}
          </div>
      )}
    </Layout>
  );
}

export default Perfil;
