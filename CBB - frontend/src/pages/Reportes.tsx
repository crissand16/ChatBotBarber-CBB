import { useEffect, useState } from 'react';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import StatusMessage from '../components/StatusMessage';
import Button from '../components/Button';

import type { Usuario } from '../interfaces/UsuarioInter';
import { obtenerEspecialistas } from '../services/usuarioService';
import { descargarReporte } from '../services/reporteService';
import type { FormatoReporte, TipoReporte } from '../services/reporteService';
import { obtenerMensajeError } from '../services/apiError';

import '../App.css';

const TIPOS: { valor: TipoReporte; etiqueta: string }[] = [
  { valor: 'agendas', etiqueta: 'Citas' },
  { valor: 'facturas', etiqueta: 'Facturación' },
];

// Mismos valores que los CHECK de la base de datos (agenda y factura).
const ESTADOS: Record<TipoReporte, string[]> = {
  agendas: ['pendiente', 'aceptada', 'rechazada', 'completada', 'cancelada'],
  facturas: ['pendiente', 'pagada'],
};

// Fecha local en formato YYYY-MM-DD (toISOString usaría UTC y podría correr el día).
const aISO = (fecha: Date): string => {
  const mes = String(fecha.getMonth() + 1).padStart(2, '0');
  const dia = String(fecha.getDate()).padStart(2, '0');
  return `${fecha.getFullYear()}-${mes}-${dia}`;
};

const primerDiaDelMes = (): string => {
  const hoy = new Date();
  return aISO(new Date(hoy.getFullYear(), hoy.getMonth(), 1));
};

function Reportes() {
  const [tipo, setTipo] = useState<TipoReporte>('agendas');
  const [fechaInicio, setFechaInicio] = useState<string>(primerDiaDelMes());
  const [fechaFin, setFechaFin] = useState<string>(aISO(new Date()));
  const [estado, setEstado] = useState<string>('');
  const [idEspecialista, setIdEspecialista] = useState<string>('');

  const [especialistas, setEspecialistas] = useState<Usuario[]>([]);
  const [descargando, setDescargando] = useState<FormatoReporte | null>(null);
  const [error, setError] = useState<string>('');
  const [exito, setExito] = useState<string>('');

  useEffect(() => {
    const cargarEspecialistas = async () => {
      try {
        
        setEspecialistas(await obtenerEspecialistas());
      } catch (err) {
        setError(obtenerMensajeError(err, 'No se pudo cargar la lista de especialistas.'));
      }
    };

    cargarEspecialistas();
  }, []);

  const cambiarTipo = (nuevoTipo: TipoReporte) => {
    setTipo(nuevoTipo);
    // Los estados válidos dependen del tipo de reporte.
    setEstado('');
    setError('');
    setExito('');
  };

  const manejarDescarga = async (formato: FormatoReporte) => {
    setError('');
    setExito('');

    if (!fechaInicio || !fechaFin) {
      setError('Selecciona la fecha inicial y la fecha final.');
      return;
    }
    if (fechaInicio > fechaFin) {
      setError('La fecha inicial no puede ser mayor que la fecha final.');
      return;
    }

    setDescargando(formato);
    try {
      await descargarReporte(tipo, formato, {
        fechaInicio,
        fechaFin,
        estado,
        idEspecialista,
      });
      setExito(`Reporte ${formato === 'excel' ? 'Excel' : 'PDF'} descargado correctamente.`);
    } catch (err) {
      setError(obtenerMensajeError(err, 'No se pudo generar el reporte.'));
    } finally {
      setDescargando(null);
    }
  };

  return (
    <Layout>
      <PageHeader
        eyebrow="Panel administrativo"
        title="Reportes"
        description="Genera reportes de citas o facturación y descárgalos en Excel o PDF."
      />

      <div className="tabs-filtro">
        {TIPOS.map((opcion) => (
          <button
            type="button"
            key={opcion.valor}
            className={'tab-btn' + (tipo === opcion.valor ? ' activo' : '')}
            onClick={() => cambiarTipo(opcion.valor)}
          >
            {opcion.etiqueta}
          </button>
        ))}
      </div>

      <div className="panel-form">
        <h3 className="panel-form-titulo">
          {tipo === 'agendas' ? 'Reporte de citas' : 'Reporte de facturación'}
        </h3>

        <div className="panel-form-grid">
          <div className="form-group">
            <label htmlFor="reporte_desde">Desde</label>
            <input
              id="reporte_desde"
              type="date"
              value={fechaInicio}
              onChange={(e) => setFechaInicio(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="reporte_hasta">Hasta</label>
            <input
              id="reporte_hasta"
              type="date"
              value={fechaFin}
              onChange={(e) => setFechaFin(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="reporte_estado">Estado</label>
            <select
              id="reporte_estado"
              value={estado}
              onChange={(e) => setEstado(e.target.value)}
            >
              <option value="">Todos</option>
              {ESTADOS[tipo].map((valor) => (
                <option key={valor} value={valor}>
                  {valor}
                </option>
              ))}
            </select>
          </div>

          {tipo === 'agendas' && (
            <div className="form-group">
              <label htmlFor="reporte_especialista">Especialista</label>
              <select
                id="reporte_especialista"
                value={idEspecialista}
                onChange={(e) => setIdEspecialista(e.target.value)}
              >
                <option value="">Todos</option>
                {especialistas.map((especialista) => (
                  <option key={especialista.id_usuario} value={especialista.id_usuario}>
                    {especialista.nombres_usuario} {especialista.apellidos_usuario}
                   
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {error && <p className="form-error">{error}</p>}
        {exito && <StatusMessage tono="exito" titulo={exito} />}

        <div className="panel-form-acciones">
          <Button
            variant="success"
            onClick={() => manejarDescarga('excel')}
            disabled={descargando !== null}
          >
            {descargando === 'excel' ? 'Generando...' : 'Descargar Excel'}
          </Button>
          <Button
            variant="outline"
            onClick={() => manejarDescarga('pdf')}
            disabled={descargando !== null}
          >
            {descargando === 'pdf' ? 'Generando...' : 'Descargar PDF'}
          </Button>
        </div>
      </div>
    </Layout>
  );
}

export default Reportes;