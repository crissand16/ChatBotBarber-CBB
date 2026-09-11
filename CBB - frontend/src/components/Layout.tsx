import Sidebar from './Sidebar';
import type { LayoutProps } from '../interfaces/LayoutInter';

function Layout({ children }: LayoutProps) {
  return (
    <div className="app-layout">

      <Sidebar />

      <main className="main-content">
        {children}
      </main>

    </div>
  );
}

export default Layout;