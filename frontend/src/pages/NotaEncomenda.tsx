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
} from '@mui/material';
import { clientService, orderNoteService } from '../api/apiService';

const NotaEncomenda = () => {
  const [formData, setFormData] = useState({
    order_note_number: '',
    delivery_date: '',
    delivery_location: '',
    issue_date: '',
    due_date: '',
    reference: '',
    series: '',
    currency: 'AOA',
    notes: '',
    retention_percent: '',
    client_id: '',
    items: [],
    subtotal: 0,
    discount: 0,
    taxable_base: 0,
    tax: 0,
    retention: 0,
    total: 0,
  });

  const [clients, setClients] = useState<any[]>([]);
  const [filteredClients, setFilteredClients] = useState<any[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState(false);

  useEffect(() => {
    const initialize = async () => {
      try {
        const clientsData = await clientService.getClients();
        setClients(clientsData);
        setFilteredClients(clientsData);

        const nextNumber = await orderNoteService.getNextOrderNoteNumber();
        setFormData(prev => ({
          ...prev,
          order_note_number: nextNumber.order_note_number,
          issue_date: new Date().toISOString().split('T')[0],
          delivery_date: new Date().toISOString().split('T')[0],
          due_date: '45 dias',
          series: new Date().getFullYear().toString(),
        }));
      } catch (error) {}
    };
    initialize();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  // Aquí deberías agregar lógica para manejar los ítems y cálculos de totales

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    if (!formData.client_id) {
      newErrors.client_id = 'Seleccione un cliente';
    }
    // ...validaciones adicionales...
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

    try {
      const data = {
        ...formData,
        client_id: Number(formData.client_id),
        retention_percent: Number(formData.retention_percent) || 0,
        // items, subtotal, discount, taxable_base, tax, retention, total deben ser calculados
      };
      await orderNoteService.createOrderNote(data);
      setSubmitSuccess(true);
    } catch (error) {
      setSubmitError('Error al guardar la nota de encomenda.');
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Nota de Encomenda
      </Typography>
      {submitError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {submitError}
        </Alert>
      )}
      {submitSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Nota de encomenda criada exitosamente
        </Alert>
      )}
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <TextField
              label="Série"
              name="series"
              value={formData.series}
              fullWidth
              InputProps={{ readOnly: true }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Número"
              name="order_note_number"
              value={formData.order_note_number}
              fullWidth
              InputProps={{ readOnly: true }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Moeda"
              name="currency"
              value={formData.currency}
              fullWidth
              select
            >
              <MenuItem value="AOA">Angolan kwanza (AOA)</MenuItem>
              <MenuItem value="EUR">Euro (EUR)</MenuItem>
              <MenuItem value="USD">Dólar (USD)</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Data"
              name="issue_date"
              type="date"
              value={formData.issue_date}
              fullWidth
              InputLabelProps={{ shrink: true }}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Vencimento"
              name="due_date"
              value={formData.due_date}
              fullWidth
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Data de entrega"
              name="delivery_date"
              type="date"
              value={formData.delivery_date}
              fullWidth
              InputLabelProps={{ shrink: true }}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Local de entrega"
              name="delivery_location"
              value={formData.delivery_location}
              fullWidth
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="V/ Ref."
              name="reference"
              value={formData.reference}
              fullWidth
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Observações"
              name="notes"
              value={formData.notes}
              fullWidth
              multiline
              rows={2}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Retenção (%)"
              name="retention_percent"
              value={formData.retention_percent}
              fullWidth
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} md={6}>
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
          {/* Aquí deberías renderizar la tabla de ítems y el sumario de totales */}
          {/* ... */}
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
              >
                Guardar Nota de Encomenda
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
};

export default NotaEncomenda;
