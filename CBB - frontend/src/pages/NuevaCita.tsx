import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type { Servicio } from '../interfaces/ServicioInter';
import type { Usuario } from '../interfaces/UsuarioInter';
import type { FranjaReservable, PasoReserva } from '../interfaces/NuevaCitaInter';

import { obtenerServicios } from '../services/servicioService';
import { obtenerEspecialistas } from '../services/usuarioService';
import { obtenerServicioDisponibilidad } from '../services/servicioDisponibilidadService';
import { obtenerDisponibilidadRango } from '../services/disponibilidadService';
import { crearAgenda } from '../services/agendaService';
import { obtenerMensajeError } from '../services/apiError';
import { useAuth } from '../context/AuthContext';

import '../App.css';

const DIAS_VENTANA = 365;

const formatoFecha = (fecha: Date): string => {
  const anio = fecha.getFullYear();
  const mes = String(fecha.getMonth() + 1).padStart(2, '0');
  const dia = String(fecha.getDate()).padStart(2, '0');

  return `${anio}-${mes}-${dia}`;
};

const formatearFechaLarga = (fecha: string): string => {
  const [anio, mes, dia] = fecha.split('-').map(Number);
  const fechaLocal = new Date(anio, (mes ?? 1) - 1, dia ?? 1);
  return fechaLocal.toLocaleDateString('es-CO', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });
};

function NuevaCita() {
  const navigate = useNavigate();
  const { usuario } = useAuth();

  const [paso, setPaso] = useState<PasoReserva>(1);

  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [especialistas, setEspecialistas] = useState<Usuario[]>([]);
  const [franjas, setFranjas] = useState<FranjaReservable[]>([]);

  const [servicioElegido, setServicioElegido] = useState<Servicio | null>(null);
  const [especialistaFiltro, setEspecialistaFiltro] = useState<string>('todos');
  const [franjaElegida, setFranjaElegida] = useState<FranjaReservable | null>(null);

  const [cargandoServicios, setCargandoServicios] = useState<boolean>(true);
  const [cargandoFranjas, setCargandoFranjas] = useState<boolean>(false);
  const [confirmando, setConfirmando] = useState<boolean>(false);

  const [error, setError] = useState<string>('');
  const [exito, setExito] = useState<string>('');

  // -------------------------------------------------------
  // PASO 1: cargar servicios y especialistas disponibles
  // -------------------------------------------------------
  useEffect(() => {
    const cargarBase = async () => {
      try {
        const [listaServicios, listaEspecialistas] = await Promise.all([
          obtenerServicios(),
          obtenerEspecialistas(),
        ]);
        setServicios(listaServicios);
        setEspecialistas(listaEspecialistas);
      } catch (err) {
        setError(obtenerMensajeError(err, 'No se pudieron cargar los servicios.'));
      } finally {
        setCargandoServicios(false);
      }
    };

    cargarBase();
  }, []);

  // -------------------------------------------------------
  // PASO 2: al elegir servicio, cruzar servicio_disponibilidad
  // con la disponibilidad real de los especialistas
  // -------------------------------------------------------
  const elegirServicio = async (servicio: Servicio) => {
    setServicioElegido(servicio);
    setFranjaElegida(null);
    setEspecialistaFiltro('todos');
    setError('');
    setCargandoFranjas(true);
    setPaso(2);

    try {
      const hoy = new Date();
      const limite = new Date();
      limite.setDate(hoy.getDate() + DIAS_VENTANA);

      const [relaciones, disponibilidad] = await Promise.all([
        obtenerServicioDisponibilidad(),
        obtenerDisponibilidadRango(formatoFecha(hoy), formatoFecha(limite)),
      ]);

      const idsDisponibilidadHabilitados = new Map<number, number>();
      relaciones
        .filter((relacion) => relacion.id_servicios === servicio.id_servicios)
        .forEach((relacion) => {
          idsDisponibilidadHabilitados.set(
            relacion.id_disponibilidad,
            relacion.id_servicio_disponibilidad
          );
        });

      const franjasReservables: FranjaReservable[] = disponibilidad
        .filter(
          (item) =>
            item.estado_disponibilidad === 'disponible' &&
            idsDisponibilidadHabilitados.has(item.id_disponibilidad)
        )
        .map((item) => ({
          ...item,
          id_servicio_disponibilidad: idsDisponibilidadHabilitados.get(
            item.id_disponibilidad
          )!,
        }));

      setFranjas(franjasReservables);
    } catch (err) {
      setError(
        obtenerMensajeError(err, 'No se pudo consultar la disponibilidad de horarios.')
      );
    } finally {
      setCargandoFranjas(false);
    }
  };

  const franjasFiltradas = useMemo(() => {
    if (especialistaFiltro === 'todos') return franjas;
    return franjas.filter((franja) => franja.id_especialista === especialistaFiltro);
  }, [franjas, especialistaFiltro]);

  const franjasPorFecha = useMemo(() => {
    const grupos = new Map<string, FranjaReservable[]>();
    franjasFiltradas
      .slice()
      .sort((a, b) => {
        if (a.fecha_disponibilidad === b.fecha_disponibilidad) {
          return a.hora_inicio_disponibilidad.localeCompare(b.hora_inicio_disponibilidad);
        }
        return a.fecha_disponibilidad.localeCompare(b.fecha_disponibilidad);
      })
      .forEach((franja) => {
        const lista = grupos.get(franja.fecha_disponibilidad) ?? [];
        lista.push(franja);
        grupos.set(franja.fecha_disponibilidad, lista);
      });
    return Array.from(grupos.entries());
  }, [franjasFiltradas]);

  const irAConfirmar = (franja: FranjaReservable) => {
    setFranjaElegida(franja);
    setPaso(3);
  };

  // -------------------------------------------------------
  // PASO 3: confirmar y crear la agenda
  // -------------------------------------------------------
  const confirmarReserva = async () => {
    if (!usuario || !franjaElegida) return;

    setConfirmando(true);
    setError('');

    try {
      await crearAgenda({
        id_cliente: usuario.id_usuario,
        id_servicio_disponibilidad: franjaElegida.id_servicio_disponibilidad,
      });

      setExito('¡Tu cita quedó agendada con éxito!');
      setTimeout(() => navigate('/citas'), 1400);
    } catch (err) {
      setError(obtenerMensajeError(err, 'No se pudo crear la cita. Intenta nuevamente.'));
      setConfirmando(false);
    }
  };

  return (
    <Layout>
      <PageHeader
        eyebrow="Reserva en 3 pasos"
        title="Agendar nueva cita"
        description="Elige tu servicio, luego el horario que más te convenga y confirma."
      />

      <ol className="reserva-pasos">
        <li className={paso >= 1 ? 'activo' : ''}>1. Servicio</li>
        <li className={paso >= 2 ? 'activo' : ''}>2. Horario</li>
        <li className={paso >= 3 ? 'activo' : ''}>3. Confirmar</li>
      </ol>

      {error && <p className="form-error reserva-error">{error}</p>}

      {/* PASO 1 */}
      {paso === 1 && (
        <>
          {cargandoServicios && (
            <StatusMessage tono="cargando" titulo="Cargando servicios..." />
          )}

          {!cargandoServicios && servicios.length === 0 && (
            <StatusMessage
              tono="vacio"
              titulo="Aún no hay servicios publicados"
              descripcion="Vuelve más tarde para agendar tu cita."
            />
          )}

          {!cargandoServicios && servicios.length > 0 && (
            <div className="servicios-grid">
              {servicios.map((servicio) => (
                <button
                  type="button"
                  key={servicio.id_servicios}
                  className={
                    'servicio-card servicio-card-elegible' +
                    (servicioElegido?.id_servicios === servicio.id_servicios
                      ? ' seleccionado'
                      : '')
                  }
                  onClick={() => elegirServicio(servicio)}
                >
                  <h3>{servicio.nombre_servicio}</h3>
                  {servicio.descripcion_servicio && <p>{servicio.descripcion_servicio}</p>}
                  <div className="servicio-meta">
                    <span>${servicio.precio_servicio.toLocaleString('es-CO')}</span>
                    <span>{servicio.duracion_minutos_servicio} min</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </>
      )}

      {/* PASO 2 */}
      {paso === 2 && servicioElegido && (
        <section className="reserva-horarios">
          <div className="reserva-resumen-chip">
            <span>Servicio elegido:</span>
            <strong>{servicioElegido.nombre_servicio}</strong>
            <button type="button" className="link-cambiar" onClick={() => setPaso(1)}>
              Cambiar
            </button>
          </div>

          {especialistas.length > 0 && (
            <div className="reserva-filtro-especialista">
              <label htmlFor="especialista">Especialista</label>
              <select
                id="especialista"
                value={especialistaFiltro}
                onChange={(e) => setEspecialistaFiltro(e.target.value)}
              >
                <option value="todos">Cualquier especialista</option>
                {especialistas.map((especialista) => (
                  <option key={especialista.id_usuario} value={especialista.id_usuario}>
                    {especialista.nombres_usuario} {especialista.apellidos_usuario}
                  </option>
                ))}
              </select>
            </div>
          )}

          {cargandoFranjas && (
            <StatusMessage tono="cargando" titulo="Buscando horarios disponibles..." />
          )}

          {!cargandoFranjas && franjasPorFecha.length === 0 && (
            <StatusMessage
              tono="vacio"
              titulo="No hay horarios disponibles"
              descripcion="Prueba con otro especialista o vuelve a intentarlo más tarde."
            />
          )}

          {!cargandoFranjas &&
            franjasPorFecha.map(([fecha, lista]) => (
              <div className="reserva-dia" key={fecha}>
                <h4>{formatearFechaLarga(fecha)}</h4>
                <div className="reserva-slots">
                  {lista.map((franja) => (
                    <button
                      type="button"
                      key={franja.id_disponibilidad}
                      className="reserva-slot"
                      onClick={() => irAConfirmar(franja)}
                    >
                      <strong>{franja.hora_inicio_disponibilidad.slice(0, 5)}</strong>
                      <span>
                        {franja.nombres_usuario} {franja.apellidos_usuario}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
        </section>
      )}

      {/* PASO 3 */}
      {paso === 3 && servicioElegido && franjaElegida && (
        <section className="reserva-confirmar">
          {exito ? (
            <StatusMessage tono="exito" titulo={exito} />
          ) : (
            <>
              <div className="reserva-confirmar-card">
                <h3>Revisa los datos de tu cita</h3>

                <dl>
                  <div>
                    <dt>Servicio</dt>
                    <dd>{servicioElegido.nombre_servicio}</dd>
                  </div>
                  <div>
                    <dt>Precio</dt>
                    <dd>${servicioElegido.precio_servicio.toLocaleString('es-CO')}</dd>
                  </div>
                  <div>
                    <dt>Especialista</dt>
                    <dd>
                      {franjaElegida.nombres_usuario} {franjaElegida.apellidos_usuario}
                    </dd>
                  </div>
                  <div>
                    <dt>Fecha</dt>
                    <dd>{formatearFechaLarga(franjaElegida.fecha_disponibilidad)}</dd>
                  </div>
                  <div>
                    <dt>Hora</dt>
                    <dd>{franjaElegida.hora_inicio_disponibilidad.slice(0, 5)}</dd>
                  </div>
                </dl>

                <div className="reserva-confirmar-acciones">
                  <Button variant="outline" onClick={() => setPaso(2)} disabled={confirmando}>
                    Volver
                  </Button>
                  <Button variant="success" onClick={confirmarReserva} disabled={confirmando}>
                    {confirmando ? 'Confirmando...' : 'Confirmar cita'}
                  </Button>
                </div>
              </div>
            </>
          )}
        </section>
      )}
    </Layout>
  );
}

export default NuevaCita;
