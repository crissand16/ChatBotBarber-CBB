import type { StatusMessageProps } from '../interfaces/StatusMessageInter';

const ICONOS: Record<StatusMessageProps['tono'], string> = {
  cargando: '',
  error: '⚠️',
  vacio: '🗂️',
  exito: '✅',
};

function StatusMessage({ tono, titulo, descripcion }: StatusMessageProps) {
  return (
    <div className={`status-message status-${tono}`}>
      {tono === 'cargando' ? (
        <span className="status-spinner" aria-hidden="true" />
      ) : (
        <span className="status-icon" aria-hidden="true">
          {ICONOS[tono]}
        </span>
      )}
      <div>
        <strong>{titulo}</strong>
        {descripcion && <p>{descripcion}</p>}
      </div>
    </div>
  );
}

export default StatusMessage;
