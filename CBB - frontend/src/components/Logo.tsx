import logo from '../assets/logo.svg';

interface LogoProps {
  size?: number;
  className?: string;
}

// Para poner tu logo real: reemplaza el archivo
// src/assets/logo.svg por el tuyo (mismo nombre), o si tu logo
// es .png/.jpg, cambia el import de arriba a "../assets/logo.png".
function Logo({ size = 56, className = '' }: LogoProps) {
  return (
    <img
      src={logo}
      alt="Logo ChatBotBarber"
      className={`logo ${className}`.trim()}
      style={{ width: size, height: size }}
    />
  );
}

export default Logo;
