import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { CssBaseline, ThemeProvider } from '@mui/material';
import theme from './styles/theme';
import { BrowserRouter } from 'react-router-dom';
import './index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);
