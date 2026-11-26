import type { ButtonProps } from '../interfaces/ButtonInter';

function Button({
  children,
  type = 'button',
  variant = 'success',
  disabled = false,
  onClick,
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`btn btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export default Button;
