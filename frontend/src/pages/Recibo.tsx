import React, { useState, useEffect } from 'react';
import {
  TextField,
  Button,
  Grid,
  Container,
  Typography,
  MenuItem,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { clientService, receiptService } from '../api/apiService';

const Recibo = () => {
  const [formData, setFormData] = useState({
    receipt_number: '',
    issue_date: new Date().toISOString().split('T')[0],
    client_id: '',
    client_name: '',
    client_address: '',
    client_tax_id: '',
    total_amount: '',
  });

  const [clients, setClients] = useState<any[]>([]);
  const [filteredClients, setFilteredClients] = useState<any[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [loading, setLoading] = useState({
    clients: false,
    submit: false,
  });

  useEffect(() => {
    const initializeReceipt = async () => {
      try {
        setLoading(prev => ({ ...prev, clients: true }));
        const clientsData = await clientService.getClients();
        setClients(clientsData);
        setFilteredClients(clientsData);
        setLoading(prev => ({ ...prev, clients: false }));

        const nextNumber = await receiptService.getNextReceiptNumber();
        setFormData(prev => ({
          ...prev,
          receipt_number: nextNumber.receipt_number
        }));
      } catch (error) {
        setLoading(prev => ({ ...prev, clients: false }));
      }
    };
    initializeReceipt();
  }, []);

  const filterClients = (inputValue: string) => {
    const filtered = clients.filter(client =>
      client.nif.toLowerCase().includes(inputValue.toLowerCase()) ||
      client.name.toLowerCase().includes(inputValue.toLowerCase())
    );
    setFilteredClients(filtered);
  };

  const handleClientSelect = (event: any, value: any) => {
    if (value) {
      setFormData(prev => ({
        ...prev,
        client_id: value.id,
        client_name: value.name,
        client_address: value.address,
        client_tax_id: value.nif,
      }));
      setErrors(prev => ({ ...prev, client_id: '' }));
    } else {
      setFormData(prev => ({
        ...prev,
        client_id: '',
        client_name: '',
        client_address: '',
        client_tax_id: '',
      }));
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    if (!formData.client_id) {
      newErrors.client_id = 'Seleccione un cliente';
    }
    if (!formData.total_amount || isNaN(Number(formData.total_amount))) {
      newErrors.total_amount = 'Ingrese un importe válido';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError('');
    setSubmitSuccess(false);

    if (!validateForm()) {
      return;
    }

    setLoading(prev => ({ ...prev, submit: true }));
    try {
      const receiptData = {
        ...formData,
        total_amount: Number(formData.total_amount),
        client_id: Number(formData.client_id),
      };
      await receiptService.createReceipt(receiptData);
      setSubmitSuccess(true);
    } catch (error) {
      setSubmitError('Error al guardar el recibo.');
    } finally {
      setLoading(prev => ({ ...prev, submit: false }));
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Factura-Recibo
      </Typography>
      {submitError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {submitError}
        </Alert>
      )}
      {submitSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Recibo creado exitosamente
        </Alert>
      )}
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              label="Número de Recibo"
              name="receipt_number"
              value={formData.receipt_number}
              fullWidth
              InputProps={{ readOnly: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Fecha de Emisión"
              name="issue_date"
              type="date"
              value={formData.issue_date}
              fullWidth
              InputLabelProps={{ shrink: true }}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              select
              label="Cliente"
              name="client_id"
              value={formData.client_id}
              onChange={handleChange}
              fullWidth
              error={!!errors.client_id}
              helperText={errors.client_id}
            >
              {filteredClients.map((client) => (
                <MenuItem key={client.id} value={client.id}>
                  {client.nif} - {client.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Importe Total"
              name="total_amount"
              value={formData.total_amount}
              onChange={handleChange}
              fullWidth
              error={!!errors.total_amount}
              helperText={errors.total_amount}
            />
          </Grid>
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading.submit}
              >
                Guardar Recibo
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
};

export default Recibo;
