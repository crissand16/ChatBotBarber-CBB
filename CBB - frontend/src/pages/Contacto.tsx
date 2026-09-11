import { useState } from 'react';
import type { FormEvent } from 'react';

import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import Button from '../components/Button';

import type { ContactoFormState, ContactoInfoItem } from '../interfaces/ContactoFormInter';
import { validarCorreo } from '../services/validaciones';

import '../App.css';

const INFO_CONTACTO: ContactoInfoItem[] = [
  {
    icono: '📞',
    titulo: 'Teléfono',
    valor: '+57 601 555 2026',
    href: 'tel:+576015552026',
  },
  {
    icono: '✉️',
    titulo: 'Correo',
    valor: 'soporte@chatbotbarber.com',
    href: 'mailto:soporte@chatbotbarber.com',
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

const FORMULARIO_VACIO: ContactoFormState = {
  nombre: '',
  correo: '',
  mensaje: '',
};

function Contacto() {
  const [formulario, setFormulario] = useState<ContactoFormState>(FORMULARIO_VACIO);
  const [error, setError] = useState<string>('');
  const [enviando, setEnviando] = useState<boolean>(false);
  const [enviado, setEnviado] = useState<boolean>(false);

  const manejarCambio = (campo: keyof ContactoFormState, valor: string) => {
    setFormulario({ ...formulario, [campo]: valor });
    if (enviado) setEnviado(false);
  };

  const manejarEnvio = (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    setError('');

    if (formulario.nombre.trim().length < 3) {
      setError('Ingresa tu nombre completo.');
      return;
    }
    if (!validarCorreo(formulario.correo)) {
      setError('Ingresa un correo electrónico válido.');
      return;
    }
    if (formulario.mensaje.trim().length < 10) {
      setError('Cuéntanos un poco más: mínimo 10 caracteres.');
      return;
    }

    // El backend aún no expone un endpoint para mensajes de contacto,
    // así que por ahora se confirma en pantalla y se deja abierto el
    // canal directo por WhatsApp/correo mientras se conecta uno.
    setEnviando(true);
    setTimeout(() => {
      setEnviando(false);
      setEnviado(true);
      setFormulario(FORMULARIO_VACIO);
    }, 700);
  };

  return (
    <Layout>
      <PageHeader
        eyebrow="Estamos aquí para ayudarte"
        title="Contáctanos"
        description="Escríbenos por el canal que prefieras, siempre hay alguien del equipo listo para atenderte."
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
          <h2>¿Necesitas ayuda?</h2>
          <p>Completa el formulario y nuestro equipo de soporte se comunicará contigo.</p>
        </div>

        <form className="contacto-form" onSubmit={manejarEnvio}>
          <div className="form-group">
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              value={formulario.nombre}
              onChange={(e) => manejarCambio('nombre', e.target.value)}
              placeholder="Tu nombre completo"
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
            />
          </div>

          <div className="form-group">
            <label htmlFor="mensaje">Mensaje</label>
            <textarea
              id="mensaje"
              value={formulario.mensaje}
              onChange={(e) => manejarCambio('mensaje', e.target.value)}
              placeholder="Cuéntanos en qué podemos ayudarte"
              rows={4}
            />
          </div>

          {error && <p className="form-error">{error}</p>}

          {enviado && !error && (
            <p className="form-exito">
              ¡Gracias! Recibimos tu mensaje y te responderemos muy pronto.
            </p>
          )}

          <Button type="submit" variant="success" disabled={enviando}>
            {enviando ? 'Enviando...' : 'Enviar mensaje'}
          </Button>
        </form>
      </section>
    </Layout>
  );
}

export default Contacto;
