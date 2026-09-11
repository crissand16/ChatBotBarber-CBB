import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type { Servicio } from '../interfaces/ServicioInter';
import type { ServicioFormState } from '../interfaces/ServicioFormInter';
import { obtenerServicios, crearServicio } from '../services/servicioService';
import { obtenerMensajeError } from '../services/apiError';
import { useAuth } from '../context/AuthContext';

import '../App.css';

const FORMULARIO_VACIO: ServicioFormState = {
  nombre_servicio: '',
  precio_servicio: '',
  duracion_minutos_servicio: '',
  descripcion_servicio: '',
};

function Servicios() {
  const { usuario } = useAuth();
  const puedeGestionar = usuario?.rol === 'admin' || usuario?.rol === 'especialista';

  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [cargando, setCargando] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  const [mostrarFormulario, setMostrarFormulario] = useState<boolean>(false);
  const [formulario, setFormulario] = useState<ServicioFormState>(FORMULARIO_VACIO);
  const [errorFormulario, setErrorFormulario] = useState<string>('');
  const [guardando, setGuardando] = useState<boolean>(false);

  const cargarServicios = async () => {
    setCargando(true);
    try {
      const datos = await obtenerServicios();
      setServicios(datos);
      setError('');
    } catch (err) {
      setError(obtenerMensajeError(err, 'No se pudieron cargar los servicios.'));
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarServicios();
  }, []);

  const manejarCambio = (campo: keyof ServicioFormState, valor: string) => {
    setFormulario({ ...formulario, [campo]: valor });
  };

  const manejarEnvio = async (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    setErrorFormulario('');

    const precio = Number(formulario.precio_servicio);
    const duracion = Number(formulario.duracion_minutos_servicio);

    if (formulario.nombre_servicio.trim().length < 3) {
      setErrorFormulario('El nombre debe tener mínimo 3 caracteres.');
      return;
    }
    if (!precio || precio <= 0) {
      setErrorFormulario('Ingresa un precio válido.');
      return;
    }
    if (!duracion || duracion <= 0) {
      setErrorFormulario('Ingresa una duración válida en minutos.');
      return;
    }

    setGuardando(true);
    try {
      await crearServicio({
        nombre_servicio: formulario.nombre_servicio.trim(),
        precio_servicio: precio,
        duracion_minutos_servicio: duracion,
        descripcion_servicio: formulario.descripcion_servicio.trim(),
      });
      setFormulario(FORMULARIO_VACIO);
      setMostrarFormulario(false);
      await cargarServicios();
    } catch (err) {
      setErrorFormulario(obtenerMensajeError(err, 'No se pudo crear el servicio.'));
    } finally {
      setGuardando(false);
    }
  };

  return (
    <Layout>
      <PageHeader
        eyebrow="Catálogo"
        title="Servicios"
        description="Cortes, tratamientos y experiencias disponibles para agendar."
        actions={
          puedeGestionar && (
            <Button variant="outline" onClick={() => setMostrarFormulario((v) => !v)}>
              {mostrarFormulario ? 'Cancelar' : '+ Agregar servicio'}
            </Button>
          )
        }
      />

      {mostrarFormulario && puedeGestionar && (
        <form className="panel-form" onSubmit={manejarEnvio}>
          <div className="panel-form-grid">
            <div className="form-group">
              <label htmlFor="nombre_servicio">Nombre</label>
              <input
                id="nombre_servicio"
                value={formulario.nombre_servicio}
                onChange={(e) => manejarCambio('nombre_servicio', e.target.value)}
                placeholder="Corte clásico"
              />
            </div>

            <div className="form-group">
              <label htmlFor="precio_servicio">Precio (COP)</label>
              <input
                id="precio_servicio"
                type="number"
                min="0"
                value={formulario.precio_servicio}
                onChange={(e) => manejarCambio('precio_servicio', e.target.value)}
                placeholder="35000"
              />
            </div>

            <div className="form-group">
              <label htmlFor="duracion_minutos_servicio">Duración (min)</label>
              <input
                id="duracion_minutos_servicio"
                type="number"
                min="0"
                value={formulario.duracion_minutos_servicio}
                onChange={(e) =>
                  manejarCambio('duracion_minutos_servicio', e.target.value)
                }
                placeholder="30"
              />
            </div>

            <div className="form-group panel-form-full">
              <label htmlFor="descripcion_servicio">Descripción</label>
              <input
                id="descripcion_servicio"
                value={formulario.descripcion_servicio}
                onChange={(e) => manejarCambio('descripcion_servicio', e.target.value)}
                placeholder="Breve descripción del servicio"
              />
            </div>
          </div>

          {errorFormulario && <p className="form-error">{errorFormulario}</p>}

          <Button type="submit" variant="success" disabled={guardando}>
            {guardando ? 'Guardando...' : 'Guardar servicio'}
          </Button>
        </form>
      )}

      {cargando && <StatusMessage tono="cargando" titulo="Cargando servicios..." />}

      {!cargando && error && <StatusMessage tono="error" titulo={error} />}

      {!cargando && !error && servicios.length === 0 && (
        <StatusMessage
          tono="vacio"
          titulo="Aún no hay servicios"
          descripcion="Los servicios que se publiquen aparecerán en esta sección."
        />
      )}

      {!cargando && !error && servicios.length > 0 && (
        <div className="servicios-grid">
          {servicios.map((servicio) => (
            <article key={servicio.id_servicios} className="servicio-card">
              <h3>{servicio.nombre_servicio}</h3>

              {servicio.descripcion_servicio && <p>{servicio.descripcion_servicio}</p>}

              <div className="servicio-meta">
                <span>${servicio.precio_servicio.toLocaleString('es-CO')}</span>
                <span>{servicio.duracion_minutos_servicio} min</span>
              </div>
            </article>
          ))}
        </div>
      )}
    </Layout>
  );
}

export default Servicios;
