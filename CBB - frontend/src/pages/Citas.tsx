import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type { Agenda, EstadoAgenda } from '../interfaces/AgendaInter';
import {
  obtenerAgendasPorCliente,
  obtenerAgendasPorEspecialista,
  obtenerAgendasPorFecha,
  cambiarEstadoAgenda,
  anularAgenda,
} from '../services/agendaService';
import { obtenerMensajeError } from '../services/apiError';
import { useAuth } from '../context/AuthContext';

import '../App.css';

// Antes solo cubría 'pendiente' | 'confirmada' | 'cancelada', pero
// 'confirmada' nunca existe en la base de datos (los estados reales son
// pendiente/aceptada/rechazada/completada/cancelada, ver chk_agenda_estado).
// Como resultado, aceptada/rechazada/completada caían siempre en el
// badge por defecto ("pendiente"), mostrando información incorrecta.
const ESTADO_A_CLASE: Record<string, string> = {
  pendiente: 'badge-pendiente',
  aceptada: 'badge-confirmada',
  completada: 'badge-confirmada',
  rechazada: 'badge-cancelada',
  cancelada: 'badge-cancelada',
};

const hoyISO = (): string => new Date().toISOString().slice(0, 10);

function Citas() {
  const navigate = useNavigate();
  const { usuario } = useAuth();
  const esAdmin = usuario?.rol === 'admin';
  const esEspecialista = usuario?.rol === 'especialista';

  const [agendas, setAgendas] = useState<Agenda[]>([]);
  const [cargando, setCargando] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [fechaFiltro, setFechaFiltro] = useState<string>(hoyISO());
  const [idEnProceso, setIdEnProceso] = useState<number | null>(null);

  const cargarAgendas = async () => {
    if (!usuario) return;

    setCargando(true);
    setError('');

    try {
      let datos: Agenda[] = [];

      if (esAdmin) {
        datos = await obtenerAgendasPorFecha(fechaFiltro);
      } else if (esEspecialista) {
        datos = await obtenerAgendasPorEspecialista(usuario.id_usuario);
      } else {
        datos = await obtenerAgendasPorCliente(usuario.id_usuario);
      }

      setAgendas(datos);
    } catch (err) {
      setAgendas([]);
      setError(obtenerMensajeError(err, 'No se pudieron cargar las citas.'));
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarAgendas();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [usuario, esAdmin, esEspecialista, fechaFiltro]);

  const manejarCambioEstado = async (idAgenda: number, nuevoEstado: EstadoAgenda) => {
    setIdEnProceso(idAgenda);
    setError('');
    try {
      await cambiarEstadoAgenda(idAgenda, nuevoEstado);
      await cargarAgendas();
    } catch (err) {
      setError(obtenerMensajeError(err, 'No se pudo actualizar el estado de la cita.'));
    } finally {
      setIdEnProceso(null);
    }
  };

  const manejarCancelar = async (idAgenda: number) => {
    const confirmado = window.confirm('¿Seguro que quieres cancelar esta cita?');
    if (!confirmado) return;

    setIdEnProceso(idAgenda);
    setError('');
    try {
      await anularAgenda(idAgenda);
      await cargarAgendas();
    } catch (err) {
      setError(obtenerMensajeError(err, 'No se pudo cancelar la cita.'));
    } finally {
      setIdEnProceso(null);
    }
  };

  const titulo = esAdmin ? 'Citas del día' : esEspecialista ? 'Mi agenda' : 'Mis citas';
  const descripcion = esAdmin
    ? 'Consulta todas las citas agendadas para una fecha específica.'
    : esEspecialista
      ? 'Estas son las citas que tienes programadas con tus clientes.'
      : 'Consulta el estado de tus citas y agenda una nueva cuando quieras.';

  return (
    <Layout>
      <PageHeader
        eyebrow="Agenda"
        title={titulo}
        description={descripcion}
        actions={
          !esAdmin &&
          !esEspecialista && (
            <Button variant="success" onClick={() => navigate('/citas/nueva')}>
              + Nueva cita
            </Button>
          )
        }
      />

      {esAdmin && (
        <div className="reserva-filtro-especialista citas-filtro-fecha">
          <label htmlFor="fecha-citas">Fecha</label>
          <input
            id="fecha-citas"
            type="date"
            value={fechaFiltro}
            onChange={(e) => setFechaFiltro(e.target.value)}
          />
        </div>
      )}

      {cargando && <StatusMessage tono="cargando" titulo="Cargando citas..." />}

      {!cargando && error && <StatusMessage tono="error" titulo={error} />}

      {!cargando && !error && agendas.length === 0 && (
        <StatusMessage
          tono="vacio"
          titulo="No hay citas para mostrar"
          descripcion={
            esAdmin || esEspecialista
              ? 'Prueba con otra fecha.'
              : 'Agenda tu primera cita cuando quieras.'
          }
        />
      )}

      {!cargando && !error && agendas.length > 0 && (
        <div className="citas-lista">
          {agendas.map((agenda) => {
            const enProceso = idEnProceso === agenda.id_agenda;
            const puedeGestionar = esAdmin || esEspecialista;
            const puedeCancelarCliente =
              !puedeGestionar &&
              (agenda.estado_agenda === 'pendiente' || agenda.estado_agenda === 'aceptada');

            return (
              <article key={agenda.id_agenda} className="cita-card">
                <div className="cita-card-header">
                  <strong>{agenda.fecha_agenda ?? 'Sin fecha'}</strong>
                  <span>{agenda.hora_agenda ?? ''}</span>
                  <span
                    className={
                      'badge ' + (ESTADO_A_CLASE[agenda.estado_agenda] ?? 'badge-pendiente')
                    }
                  >
                    {agenda.estado_agenda}
                  </span>
                </div>

                <p>
                  {esEspecialista ? 'Con ' : 'Especialista: '}
                  {esEspecialista ? agenda.cliente.nombre : agenda.especialista.nombre}
                </p>

                <ul>
                  {agenda.servicios.map((servicio) => (
                    <li key={servicio.id_servicio}>
                      {servicio.nombre} — ${servicio.precio.toLocaleString('es-CO')}
                    </li>
                  ))}
                </ul>

                <div className="cita-card-footer">
                  <strong>Total: ${agenda.precio_total.toLocaleString('es-CO')}</strong>

                  <div className="cita-card-acciones">
                    {puedeCancelarCliente && (
                      <Button
                        variant="danger"
                        disabled={enProceso}
                        onClick={() => manejarCancelar(agenda.id_agenda)}
                      >
                        {enProceso ? 'Cancelando...' : 'Cancelar cita'}
                      </Button>
                    )}

                    {puedeGestionar && agenda.estado_agenda === 'pendiente' && (
                      <>
                        <Button
                          variant="success"
                          disabled={enProceso}
                          onClick={() => manejarCambioEstado(agenda.id_agenda, 'aceptada')}
                        >
                          Confirmar
                        </Button>
                        <Button
                          variant="danger"
                          disabled={enProceso}
                          onClick={() => manejarCambioEstado(agenda.id_agenda, 'rechazada')}
                        >
                          Rechazar
                        </Button>
                      </>
                    )}

                    {puedeGestionar && agenda.estado_agenda === 'aceptada' && (
                      <>
                        <Button
                          variant="success"
                          disabled={enProceso}
                          onClick={() => manejarCambioEstado(agenda.id_agenda, 'completada')}
                        >
                          Marcar completada
                        </Button>
                        <Button
                          variant="danger"
                          disabled={enProceso}
                          onClick={() => manejarCambioEstado(agenda.id_agenda, 'cancelada')}
                        >
                          Cancelar
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </Layout>
  );
}

export default Citas;
