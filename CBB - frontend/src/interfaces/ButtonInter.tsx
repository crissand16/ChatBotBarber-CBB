import type { ReactNode } from 'react';

// 'success' (verde) = acciones normales/positivas.
// 'danger'  (rojo)  = acciones peligrosas (cancelar, eliminar, etc.).
// 'outline' = acción secundaria neutra (azul rey).
export type ButtonVariant = 'success' | 'danger' | 'outline';

export interface ButtonProps {
  children: ReactNode;
  type?: 'button' | 'submit' | 'reset';
  variant?: ButtonVariant;
  disabled?: boolean;
  onClick?: () => void;
}
