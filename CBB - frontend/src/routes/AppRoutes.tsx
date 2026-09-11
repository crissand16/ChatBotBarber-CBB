import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Login from '../pages/Login';
import Registro from '../pages/Registro';
import Inicio from '../pages/Inicio';

import Chat from '../pages/Chat';
import Citas from '../pages/Citas';
import NuevaCita from '../pages/NuevaCita';
import Servicios from '../pages/Servicios';
import Perfil from '../pages/Perfil';
import Contacto from '../pages/Contacto';
import Equipo from '../pages/Equipo';

import RutaProtegida from './RutaProtegida';

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Navigate to="/inicio" replace />} />

        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />

        <Route
          path="/inicio"
          element={
            <RutaProtegida>
              <Inicio />
            </RutaProtegida>
          }
        />

        <Route
          path="/chat"
          element={
            <RutaProtegida>
              <Chat />
            </RutaProtegida>
          }
        />

        <Route
          path="/citas"
          element={
            <RutaProtegida>
              <Citas />
            </RutaProtegida>
          }
        />

        <Route
          path="/citas/nueva"
          element={
            <RutaProtegida>
              <NuevaCita />
            </RutaProtegida>
          }
        />

        <Route
          path="/servicios"
          element={
            <RutaProtegida>
              <Servicios />
            </RutaProtegida>
          }
        />

        <Route
          path="/usuarios"
          element={
            <RutaProtegida>
              <Equipo />
            </RutaProtegida>
          }
        />

        <Route
          path="/perfil"
          element={
            <RutaProtegida>
              <Perfil />
            </RutaProtegida>
          }
        />

        <Route
          path="/contacto"
          element={
            <RutaProtegida>
              <Contacto />
            </RutaProtegida>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
