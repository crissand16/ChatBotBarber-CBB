import type { NavbarProps } from '../interfaces/NavbarInter';

// Barra superior que SOLO se muestra en pantallas angostas (ver
// @media max-width: 640px en App.css). Contiene el botón hamburguesa
// que abre/cierra el Sidebar como un panel deslizante, reutilizando
// exactamente los mismos colores y tipografía del Sidebar/Layout.
function Navbar({ menuAbierto, alAlternarMenu }: NavbarProps) {
  return (
    <header className="navbar-mobile">
      <button
        type="button"
        className={'hamburguesa' + (menuAbierto ? ' hamburguesa-abierta' : '')}
        aria-label={menuAbierto ? 'Cerrar menú' : 'Abrir menú'}
        aria-expanded={menuAbierto}
        onClick={alAlternarMenu}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <h2 className="navbar-mobile-titulo">ChatBotBarber</h2>
    </header>
  );
}

export default Navbar;
