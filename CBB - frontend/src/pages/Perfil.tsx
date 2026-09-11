import Layout from '../components/Layout';
import PageHeader from '../components/PageHeader';
import { useAuth } from '../context/AuthContext';

import '../App.css';

const ROL_ETIQUETA: Record<string, string> = {
  cliente: 'Cliente',
  especialista: 'Especialista',
  admin: 'Administrador',
};

function Perfil() {
  const { usuario } = useAuth();

  const iniciales = usuario
    ? `${usuario.nombres.charAt(0)}${usuario.apellidos.charAt(0)}`.toUpperCase()
    : '';

  return (
    <Layout>
      <PageHeader
        eyebrow="Tu cuenta"
        title="Mi perfil"
        description="Consulta la información asociada a tu cuenta de ChatBotBarber."
      />

      {usuario && (
        <div className="perfil-card">
          <div className="perfil-avatar">{iniciales}</div>

          <div className="perfil-datos">
            <h2>
              {usuario.nombres} {usuario.apellidos}
            </h2>
            <span className="badge badge-confirmada">
              {ROL_ETIQUETA[usuario.rol] ?? usuario.rol}
            </span>

            <dl className="perfil-lista">
              <div>
                <dt>Correo</dt>
                <dd>{usuario.correo}</dd>
              </div>
              <div>
                <dt>Identificador</dt>
                <dd>{usuario.id_usuario}</dd>
              </div>
            </dl>
          </div>
        </div>
      )}
    </Layout>
  );
}

export default Perfil;
