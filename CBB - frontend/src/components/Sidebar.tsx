import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ROL_ETIQUETA: Record<string, string> = {
  cliente: 'Cliente',
  especialista: 'Especialista',
  admin: 'Administrador',
};

function Sidebar() {
  const navigate = useNavigate();
  const { usuario, cerrarSesion } = useAuth();

  const manejarCerrarSesion = () => {
    cerrarSesion();
    navigate('/login');
  };

  return (
    <aside className="sidebar">

      <div className="sidebar-logo">
        <h2>ChatBotBarber</h2>
        {usuario && (
          <p className="sidebar-usuario">
            {usuario.nombres} {usuario.apellidos}
            <span className="sidebar-rol">
              {ROL_ETIQUETA[usuario.rol] ?? usuario.rol}
            </span>
          </p>
        )}
      </div>

      <nav className="sidebar-menu">

        <NavLink to="/inicio">
          🏠 <span>Inicio</span>
        </NavLink>

        <NavLink to="/chat">
          🤖 <span>ChatBot</span>
        </NavLink>

        <NavLink to="/citas">
          📅 <span>Citas</span>
        </NavLink>

        <NavLink to="/servicios">
          ✂️ <span>Servicios</span>
        </NavLink>

        {usuario?.rol === 'admin' && (
          <NavLink to="/usuarios">
            👥 <span>Equipo</span>
          </NavLink>
        )}

        <NavLink to="/perfil">
          👤 <span>Perfil</span>
        </NavLink>

        <NavLink to="/contacto">
          📞 <span>Contacto</span>
        </NavLink>

      </nav>

      <div className="sidebar-bottom">
        <button
          type="button"
          className="sidebar-logout"
          onClick={manejarCerrarSesion}
        >
          🚪 <span>Cerrar sesión</span>
        </button>
      </div>

    </aside>
  );
}

export default Sidebar;
