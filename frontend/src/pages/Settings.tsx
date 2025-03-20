import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, Grid, Snackbar, Alert } from '@mui/material';
import axios from 'axios';

const Settings = () => {
  const [invoicePrefix, setInvoicePrefix] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

  useEffect(() => {
    // Fetch the current invoice prefix from the backend
    const fetchSettings = async () => {
      try {
        const response = await axios.get('/api/settings/invoice-prefix');
        setInvoicePrefix(response.data.invoice_prefix || '');
      } catch (error) {
        console.error('Error fetching settings:', error);
      }
    };

    fetchSettings();
  }, []);

  const handleSave = async () => {
    try {
      await axios.post('/api/settings/invoice-prefix', { invoice_prefix: invoicePrefix });
      setSnackbarMessage('Configuración guardada con éxito');
      setSnackbarSeverity('success');
      setSnackbarOpen(true);
    } catch (error) {
      console.error('Error saving settings:', error);
      setSnackbarMessage('Error al guardar la configuración');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    }
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Configuración
      </Typography>
      <Typography variant="h6" gutterBottom>
        Configurar el prefijo del código de la factura
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Prefijo del Código de Factura"
            fullWidth
            value={invoicePrefix}
            onChange={(e) => setInvoicePrefix(e.target.value)}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleSave}>
            Guardar Configuración
          </Button>
        </Grid>
      </Grid>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Settings;
