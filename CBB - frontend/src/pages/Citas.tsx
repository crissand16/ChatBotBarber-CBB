import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type { Agenda } from '../interfaces/AgendaInter';
import {
  obtenerAgendasPorCliente,
  obtenerAgendasPorEspecialista,
  obtenerAgendasPorFecha,
} from '../services/agendaService';
import { obtenerMensajeError } from '../services/apiError';
import { useAuth } from '../context/AuthContext';

import '../App.css';

const ESTADO_A_CLASE: Record<string, string> = {
  pendiente: 'badge-pendiente',
  confirmada: 'badge-confirmada',
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

  useEffect(() => {
    if (!usuario) return;

    const cargarAgendas = async () => {
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

    cargarAgendas();
  }, [usuario, esAdmin, esEspecialista, fechaFiltro]);

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
          {agendas.map((agenda) => (
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
                {!esAdmin && !esEspecialista && <Button variant="danger">Cancelar cita</Button>}
              </div>
            </article>
          ))}
        </div>
      )}
    </Layout>
  );
}

export default Citas;
