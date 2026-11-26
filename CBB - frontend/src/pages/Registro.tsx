import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import type { FormEvent } from 'react';

import type { RegistroForm } from '../interfaces/RegistroForm';

import {
  validarCorreo,
  validarPassword,
  validarTelefono,
} from '../services/validaciones';
import { registrarUsuario } from '../services/usuarioService';
import { obtenerMensajeError } from '../services/apiError';
import Logo from '../components/Logo';

import '../App.css';

function Registro() {
  const navigate = useNavigate();

  const [formulario, setFormulario] =
    useState<RegistroForm>({
      documento: '',
      nombres: '',
      apellidos: '',
      correo: '',
      telefono: '',
      fechaNacimiento: '',
      password: '',
      confirmarPassword: '',
    });

  const [error, setError] = useState<string>('');
  const [cargando, setCargando] = useState<boolean>(false);

  const manejarCambio = (
    campo: keyof RegistroForm,
    valor: string
  ) => {
    setFormulario({
      ...formulario,
      [campo]: valor,
    });
  };

  const manejarEnvio = async (
    evento: FormEvent<HTMLFormElement>
  ) => {
    evento.preventDefault();

    setError('');

    if (formulario.documento.trim().length < 3) {
      setError('Ingrese un número de documento válido.');
      return;
    }

    if (formulario.nombres.trim().length < 3) {
      setError(
        'El nombre debe tener mínimo 3 caracteres.'
      );
      return;
    }

    if (formulario.apellidos.trim().length < 3) {
      setError(
        'El apellido debe tener mínimo 3 caracteres.'
      );
      return;
    }

    if (!validarCorreo(formulario.correo)) {
      setError(
        'Ingrese un correo electrónico válido.'
      );
      return;
    }

    if (!validarTelefono(formulario.telefono)) {
      setError(
        'Ingrese un número de teléfono válido.'
      );
      return;
    }

    if (!formulario.fechaNacimiento) {
      setError('Ingrese su fecha de nacimiento.');
      return;
    }

    if (!validarPassword(formulario.password)) {
      setError(
        'La contraseña debe tener mínimo 6 caracteres.'
      );
      return;
    }

    if (
      formulario.password !==
      formulario.confirmarPassword
    ) {
      setError('Las contraseñas no coinciden.');
      return;
    }

    setCargando(true);

    try {
      await registrarUsuario({
        id_usuario: formulario.documento,
        nombres_usuario: formulario.nombres,
        apellidos_usuario: formulario.apellidos,
        correo_usuario: formulario.correo,
        contrasena_usuario: formulario.password,
        fecha_nacimiento_usuario: formulario.fechaNacimiento,
        telefono_usuario: formulario.telefono,
      });

      navigate('/login');
    } catch (err) {
      setError(obtenerMensajeError(err, 'No se pudo completar el registro.'));
    } finally {
      setCargando(false);
    }
  };

  return (
    <main className="auth-page">

      <section className="auth-card registro-card">

        <div className="auth-header">

          <Logo size={64} />

          <h1>Crear cuenta</h1>

          <p>
            Regístrate en ChatBotBarber
          </p>

        </div>

        <form
          className="auth-form"
          onSubmit={manejarEnvio}
        >

          <div className="form-group">

            <label htmlFor="documento">
              Número de documento
            </label>

            <input
              type="text"
              id="documento"
              value={formulario.documento}
              onChange={(e) =>
                manejarCambio(
                  'documento',
                  e.target.value
                )
              }
              placeholder="Ingrese su documento"
            />

          </div>

          <div className="form-group">

            <label htmlFor="nombres">
              Nombres
            </label>

            <input
              type="text"
              id="nombres"
              value={formulario.nombres}
              onChange={(e) =>
                manejarCambio(
                  'nombres',
                  e.target.value
                )
              }
              placeholder="Ingrese sus nombres"
            />

          </div>

          <div className="form-group">

            <label htmlFor="apellidos">
              Apellidos
            </label>

            <input
              type="text"
              id="apellidos"
              value={formulario.apellidos}
              onChange={(e) =>
                manejarCambio(
                  'apellidos',
                  e.target.value
                )
              }
              placeholder="Ingrese sus apellidos"
            />

          </div>

          <div className="form-group">

            <label htmlFor="correo">
              Correo electrónico
            </label>

            <input
              type="email"
              id="correo"
              value={formulario.correo}
              onChange={(e) =>
                manejarCambio(
                  'correo',
                  e.target.value
                )
              }
              placeholder="correo@ejemplo.com"
            />

          </div>

          <div className="form-group">

            <label htmlFor="telefono">
              Teléfono
            </label>

            <input
              type="tel"
              id="telefono"
              value={formulario.telefono}
              onChange={(e) =>
                manejarCambio(
                  'telefono',
                  e.target.value
                )
              }
              placeholder="Ingrese su teléfono"
            />

          </div>

          <div className="form-group">

            <label htmlFor="fechaNacimiento">
              Fecha de nacimiento
            </label>

            <input
              type="date"
              id="fechaNacimiento"
              value={formulario.fechaNacimiento}
              onChange={(e) =>
                manejarCambio(
                  'fechaNacimiento',
                  e.target.value
                )
              }
            />

          </div>

          <div className="form-group">

            <label htmlFor="password">
              Contraseña
            </label>

            <input
              type="password"
              id="password"
              value={formulario.password}
              onChange={(e) =>
                manejarCambio(
                  'password',
                  e.target.value
                )
              }
              placeholder="Mínimo 6 caracteres"
            />

          </div>

          <div className="form-group">

            <label htmlFor="confirmarPassword">
              Confirmar contraseña
            </label>

            <input
              type="password"
              id="confirmarPassword"
              value={formulario.confirmarPassword}
              onChange={(e) =>
                manejarCambio(
                  'confirmarPassword',
                  e.target.value
                )
              }
              placeholder="Repita su contraseña"
            />

          </div>

          {error && (
            <p className="form-error">
              {error}
            </p>
          )}

          <button
            type="submit"
            className="btn btn-success auth-button"
            disabled={cargando}
          >
            {cargando ? 'Creando cuenta...' : 'Crear cuenta'}
          </button>

        </form>

        <div className="auth-footer">

          <span>
            ¿Ya tienes una cuenta?
          </span>

          <Link to="/login">
            Iniciar sesión
          </Link>

        </div>

      </section>

    </main>
  );
}

export default Registro;
