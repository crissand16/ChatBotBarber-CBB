import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { UsuarioLogin } from '../interfaces/UsuarioInter';

interface AuthContextValue {
  usuario: UsuarioLogin | null;
  iniciarSesion: (usuario: UsuarioLogin) => void;
  cerrarSesion: () => void;
}

const STORAGE_KEY = 'cbb_usuario';

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const leerUsuarioGuardado = (): UsuarioLogin | null => {
  const guardado = localStorage.getItem(STORAGE_KEY);
  if (!guardado) return null;
  try {
    return JSON.parse(guardado) as UsuarioLogin;
  } catch {
    return null;
  }
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<UsuarioLogin | null>(leerUsuarioGuardado);

  const iniciarSesion = (nuevoUsuario: UsuarioLogin) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nuevoUsuario));
    setUsuario(nuevoUsuario);
  };

  const cerrarSesion = () => {
    localStorage.removeItem(STORAGE_KEY);
    setUsuario(null);
  };

  return (
    <AuthContext.Provider value={{ usuario, iniciarSesion, cerrarSesion }}>
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const contexto = useContext(AuthContext);
  if (!contexto) {
    throw new Error('useAuth debe usarse dentro de <AuthProvider>');
  }
  return contexto;
}
