import { useState } from 'react';
import type { FormEvent } from 'react';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import Button from '../components/Button';

import type {
  ContactoFormState,
  ContactoInfoItem,
  PqrTipoOpcion,
} from '../interfaces/ContactoFormInter';
import type { Pqr } from '../interfaces/PqrInter';
import { enviarPqr } from '../services/pqrService';
import { obtenerMensajeError } from '../services/apiError';
import { validarPqr } from '../services/validaciones';
import { useAuth } from '../context/AuthContext';

import '../App.css';

// Las PQR llegan a este correo y se responden desde ahí (ver backend:
// PQR_DESTINATARIO en el .env).
const CORREO_BUZON = 'adminchatbotbarber@gmail.com';

const INFO_CONTACTO: ContactoInfoItem[] = [
  {
    icono: '📞',
    titulo: 'Teléfono',
    valor: '+57 601 555 2026',
    href: 'tel:+576015552026',
  },
  {
    icono: '✉️',
    titulo: 'Correo del buzón',
    valor: CORREO_BUZON,
    href: `mailto:${CORREO_BUZON}`,
  },
  {
    icono: '🕒',
    titulo: 'Horario',
    valor: 'Lun - Vie · 9:00 a.m. - 7:00 p.m.',
  },
  {
    icono: '💬',
    titulo: 'WhatsApp',
    valor: '+57 300 555 2026',
    href: 'https://wa.me/573005552026',
  },
];

const TIPOS_PQR: PqrTipoOpcion[] = [
  {
    valor: 'peticion',
    icono: '🙋',
    titulo: 'Petición',
    descripcion: 'Solicita información o un servicio.',
  },
  {
    valor: 'queja',
    icono: '😕',
    titulo: 'Queja',
    descripcion: 'Inconformidad con la atención recibida.',
  },
  {
    valor: 'reclamo',
    icono: '⚠️',
    titulo: 'Reclamo',
    descripcion: 'Problema con un servicio o un cobro.',
  },
];

const MAX_MENSAJE = 2000;

function Contacto() {
  const { usuario } = useAuth();

  // Nombre y correo se precargan con los datos de la cuenta, pero se pueden
  // cambiar (por ejemplo, para recibir la respuesta en otro correo).
  const [formulario, setFormulario] = useState<ContactoFormState>({
    nombre: usuario ? `${usuario.nombres} ${usuario.apellidos}`.trim() : '',
    correo: usuario?.correo ?? '',
    tipo: 'peticion',
    asunto: '',
    mensaje: '',
  });
  const [error, setError] = useState<string>('');
  const [enviando, setEnviando] = useState<boolean>(false);
  const [radicada, setRadicada] = useState<Pqr | null>(null);

  const manejarCambio = (campo: keyof ContactoFormState, valor: string) => {
    setFormulario({ ...formulario, [campo]: valor });
    if (radicada) setRadicada(null);
  };

  const manejarEnvio = async (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    setError('');

    if (!usuario) return;

    const mensajeError = validarPqr(formulario);
    if (mensajeError) {
      setError(mensajeError);
      return;
    }

    setEnviando(true);
    try {
      const pqr = await enviarPqr({
        id_usuario: usuario.id_usuario,
        nombre: formulario.nombre.trim(),
        correo: formulario.correo.trim(),
        tipo: formulario.tipo,
        asunto: formulario.asunto.trim(),
        mensaje: formulario.mensaje.trim(),
      });

      setRadicada(pqr);
      // Se conservan nombre/correo/tipo; solo se limpia lo que se redactó.
      setFormulario({ ...formulario, asunto: '', mensaje: '' });
    } catch (err) {
      setError(
        obtenerMensajeError(err, 'No se pudo enviar tu solicitud. Intenta nuevamente.')
      );
    } finally {
      setEnviando(false);
    }
  };

  const tipoRadicado = TIPOS_PQR.find((t) => t.valor === radicada?.tipo_pqr);

  return (
    <Layout>
      <PageHeader
        eyebrow="Peticiones, quejas y reclamos"
        title="Contacto/buzón"
        description="Escríbenos por el canal que prefieras o deja tu solicitud en el buzón: siempre hay alguien del equipo listo para atenderte."
      />

      <div className="contacto-info-grid">
        {INFO_CONTACTO.map((item) => {
          const contenido = (
            <>
              <span className="contacto-icono" aria-hidden="true">
                {item.icono}
              </span>
              <div>
                <h3>{item.titulo}</h3>
                <p>{item.valor}</p>
              </div>
            </>
          );

          return item.href ? (
            <a
              key={item.titulo}
              href={item.href}
              target={item.href.startsWith('http') ? '_blank' : undefined}
              rel="noreferrer"
              className="contacto-info-card contacto-info-card-link"
            >
              {contenido}
            </a>
          ) : (
            <div key={item.titulo} className="contacto-info-card">
              {contenido}
            </div>
          );
        })}
      </div>

      <section className="contacto-form-section">
        <div className="contacto-form-heading">
          <h2>Buzón de PQR</h2>
          <p>
            Elige el tipo de solicitud y cuéntanos qué ocurrió. Tu mensaje llega
            directo al correo del administrador y te responderemos a tu correo.
          </p>
        </div>

        <form className="contacto-form" onSubmit={manejarEnvio}>
          <div className="form-group">
            <label>Tipo de solicitud</label>
            <div className="pqr-tipos" role="group" aria-label="Tipo de solicitud">
              {TIPOS_PQR.map((tipo) => (
                <button
                  key={tipo.valor}
                  type="button"
                  className={
                    'pqr-tipo' + (formulario.tipo === tipo.valor ? ' pqr-tipo-activo' : '')
                  }
                  aria-pressed={formulario.tipo === tipo.valor}
                  onClick={() => manejarCambio('tipo', tipo.valor)}
                >
                  <strong>
                    <span aria-hidden="true">{tipo.icono}</span> {tipo.titulo}
                  </strong>
                  <span>{tipo.descripcion}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              value={formulario.nombre}
              onChange={(e) => manejarCambio('nombre', e.target.value)}
              placeholder="Tu nombre completo"
              maxLength={100}
            />
          </div>

          <div className="form-group">
            <label htmlFor="correo-contacto">Correo electrónico</label>
            <input
              id="correo-contacto"
              type="email"
              value={formulario.correo}
              onChange={(e) => manejarCambio('correo', e.target.value)}
              placeholder="correo@ejemplo.com"
              maxLength={60}
            />
          </div>

          <div className="form-group">
            <label htmlFor="asunto">Asunto</label>
            <input
              id="asunto"
              value={formulario.asunto}
              onChange={(e) => manejarCambio('asunto', e.target.value)}
              placeholder="Resume tu solicitud en una frase"
              maxLength={120}
            />
          </div>

          <div className="form-group">
            <label htmlFor="mensaje">Mensaje</label>
            <textarea
              id="mensaje"
              value={formulario.mensaje}
              onChange={(e) => manejarCambio('mensaje', e.target.value)}
              placeholder="Cuéntanos en qué podemos ayudarte"
              rows={5}
              maxLength={MAX_MENSAJE}
            />
            <span className="form-ayuda">
              {formulario.mensaje.length}/{MAX_MENSAJE}
            </span>
          </div>

          {error && <p className="form-error">{error}</p>}

          {radicada && !error && radicada.correo_enviado_pqr && (
            <p className="form-exito">
              ¡Gracias! Radicamos tu {tipoRadicado?.titulo.toLowerCase() ?? 'solicitud'} con el
              número <strong>{radicada.radicado}</strong>. Te responderemos al correo{' '}
              {radicada.correo_pqr}.
            </p>
          )}

          {radicada && !error && !radicada.correo_enviado_pqr && (
            <p className="form-aviso">
              Radicamos tu solicitud con el número <strong>{radicada.radicado}</strong>, pero no
              pudimos enviar la notificación por correo. El equipo la revisará igualmente.
            </p>
          )}

          <Button type="submit" variant="success" disabled={enviando}>
            {enviando ? 'Enviando...' : 'Enviar al buzón'}
          </Button>
        </form>
      </section>
    </Layout>
  );
}

export default Contacto;
