import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';

import '../App.css';

function Chat() {
  return (
    <Layout>
      <PageHeader
        eyebrow="Asistente virtual"
        title="ChatBot"
        description="Resuelve dudas rápidas sobre servicios, horarios y tus citas."
      />

      <div className="chat-placeholder">
        <span className="chat-placeholder-icono" aria-hidden="true">
          🤖
        </span>
        <h3>Estamos afinando al asistente</h3>
        <p>
          Muy pronto podrás conversar aquí mismo para resolver dudas y agendar citas
          sin salir del chat. Mientras tanto, usa la sección de{' '}
          <strong>Contacto</strong> si necesitas ayuda inmediata.
        </p>
      </div>
    </Layout>
  );
}

export default Chat;
