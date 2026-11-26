import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Logo from '../components/Logo';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

const PASOS_BIENVENIDA = [
  {
    emoji: '✂️',
    titulo: 'Explora nuestros servicios',
    texto: 'Revisa precios y duración de cada corte o tratamiento antes de reservar.',
  },
  {
    emoji: '📅',
    titulo: 'Agenda tu cita',
    texto: 'Elige el especialista y el horario que mejor se ajuste a tu día.',
  },
  {
    emoji: '🤖',
    titulo: 'Resuelve dudas con el ChatBot',
    texto: '¿Tienes preguntas rápidas? Nuestro asistente virtual te ayuda al instante.',
  },
  {
    emoji: '👤',
    titulo: 'Administra tu perfil',
    texto: 'Mantén actualizados tus datos de contacto en cualquier momento.',
  },
];

function Inicio() {
  const navigate = useNavigate();
  const { usuario } = useAuth();
  const esCliente = usuario?.rol === 'cliente';

  return (
    <Layout>

      <section className="bienvenida-hero">
        <Logo size={72} />

        <h1>
          Bienvenido{usuario ? `, ${usuario.nombres}` : ''} a ChatBotBarber
        </h1>

        <p>
          Sistema de gestión y atención para barberías. Esta es una
          pequeña guía de lo que puedes hacer aquí.
        </p>

        <div className="bienvenida-acciones">
          {esCliente && (
            <Button variant="success" onClick={() => navigate('/citas/nueva')}>
              Agendar cita
            </Button>
          )}
          <Button variant={esCliente ? 'outline' : 'success'} onClick={() => navigate('/citas')}>
            Ver citas
          </Button>
          <Button variant="outline" onClick={() => navigate('/servicios')}>
            Ver servicios
          </Button>
        </div>
      </section>

      <section className="bienvenida-pasos">
        {PASOS_BIENVENIDA.map((paso) => (
          <article key={paso.titulo} className="paso-card">
            <span className="paso-emoji">{paso.emoji}</span>
            <h3>{paso.titulo}</h3>
            <p>{paso.texto}</p>
          </article>
        ))}
      </section>

    </Layout>
  );
}

export default Inicio;
