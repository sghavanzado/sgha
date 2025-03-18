//App.tsx

import { useEffect } from 'react';
import React, { useState } from 'react';
import { useNavigate, Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { AuthProvider, useAuth } from './components/AuthContext';
import SideMenu from './components/SideMenu';
import ContentArea from './components/ContentArea';
import SignInSide from './pages/SignInSide';
import LoadingBackdrop from './components/LoadingBackdrop';



// Componente principal que envuelve la aplicación con el contexto de autenticación
const AppWrapper = () => {

  const [isLoading] = useState(false); 
  // Obtiene el token y el estado de carga del contexto de autenticación
  const { token, loading } = useAuth();
  // Hook para la navegación
  const navigate = useNavigate();

  useEffect(() => {
    // Si no está cargando
    if (!loading) {
      // Si hay un token
      if (token) {
        // Navega al dashboard
        navigate('/dashboard');
      } else {
        // Navega a la página de inicio de sesión
        navigate('/');
      }
    }
  }, [token, loading, navigate]); // Dependencias del useEffect

  // Muestra un indicador de carga si está cargando
  if (loading) {
    return <LoadingBackdrop open={isLoading} />
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* Muestra el menú lateral si hay un token */}
      {token && <SideMenu />}
        <Routes>
          {/* Ruta para la página de inicio de sesión */}
          <Route path="/" element={<SignInSide />} />
          {/* Ruta para el área de contenido */}
          <Route path="/*" element={<ContentArea />} />
        </Routes>
      
    </Box>
  );
};

// Componente principal de la aplicación
const App = () => {
  return (
    // Proveedor de contexto de autenticación
    <AuthProvider>
      {/* Componente envuelto */}
      <AppWrapper />
    </AuthProvider>
  );
};

export default App;