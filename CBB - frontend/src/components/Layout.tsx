import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

import Navbar from './Navbar';
import Sidebar from './Sidebar';
import type { LayoutProps } from '../interfaces/LayoutInter';

function Layout({ children }: LayoutProps) {
  const [menuAbierto, setMenuAbierto] = useState(false);
  const { pathname } = useLocation();

  // Si el usuario navega a otra página (por ejemplo tocando un link del
  // propio menú) el panel móvil se cierra solo, en vez de quedar abierto
  // tapando la pantalla.
  useEffect(() => {
    setMenuAbierto(false);
  }, [pathname]);

  return (
    <div className="app-layout">

      <Navbar
        menuAbierto={menuAbierto}
        alAlternarMenu={() => setMenuAbierto((abierto) => !abierto)}
      />

      <Sidebar abierto={menuAbierto} onCerrar={() => setMenuAbierto(false)} />

      <main className="main-content">
        {children}
      </main>

    </div>
  );
}

export default Layout;
