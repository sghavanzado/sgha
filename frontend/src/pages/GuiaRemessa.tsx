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
import { clientService, shippingGuideService } from '../api/apiService';

const GuiaRemessa = () => {
  const [formData, setFormData] = useState({
    guide_number: '',
    issue_date: new Date().toISOString().split('T')[0],
    client_id: '',
    total_amount: '',
    vehicle_plate: '',
    load_date: '',
    load_location: '',
    load_address: '',
    load_city: '',
    load_postal_code: '',
    delivery_location: '',
    delivery_address: '',
    delivery_city: '',
    delivery_postal_code: '',
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

        const nextNumber = await shippingGuideService.getNextGuideNumber();
        setFormData(prev => ({
          ...prev,
          guide_number: nextNumber.guide_number
        }));
      } catch (error) {}
    };
    initialize();
  }, []);

  const filterClients = (inputValue: string) => {
    const filtered = clients.filter(client =>
      client.nif.toLowerCase().includes(inputValue.toLowerCase()) ||
      client.name.toLowerCase().includes(inputValue.toLowerCase())
    );
    setFilteredClients(filtered);
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
    if (!formData.vehicle_plate) {
      newErrors.vehicle_plate = 'Ingrese la matrícula';
    }
    if (!formData.load_date) {
      newErrors.load_date = 'Ingrese la fecha de carga';
    }
    if (!formData.load_location) {
      newErrors.load_location = 'Ingrese el local de carga';
    }
    if (!formData.load_address) {
      newErrors.load_address = 'Ingrese el endereço de carga';
    }
    if (!formData.load_city) {
      newErrors.load_city = 'Ingrese la ciudad de carga';
    }
    if (!formData.load_postal_code) {
      newErrors.load_postal_code = 'Ingrese la caja postal de carga';
    }
    if (!formData.delivery_location) {
      newErrors.delivery_location = 'Ingrese el local de entrega';
    }
    if (!formData.delivery_address) {
      newErrors.delivery_address = 'Ingrese el endereço de entrega';
    }
    if (!formData.delivery_city) {
      newErrors.delivery_city = 'Ingrese la ciudad de entrega';
    }
    if (!formData.delivery_postal_code) {
      newErrors.delivery_postal_code = 'Ingrese la caja postal de entrega';
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

    try {
      const data = {
        ...formData,
        total_amount: Number(formData.total_amount),
        client_id: Number(formData.client_id),
      };
      await shippingGuideService.createShippingGuide(data);
      setSubmitSuccess(true);
    } catch (error) {
      setSubmitError('Error al guardar la guía de remessa.');
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>
        Guia de Remessa
      </Typography>
      {submitError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {submitError}
        </Alert>
      )}
      {submitSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Guia de remessa creada exitosamente
        </Alert>
      )}
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              label="Número de Guia"
              name="guide_number"
              value={formData.guide_number}
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
          {/* Detalhes do transporte */}
          <Grid item xs={12}>
            <Typography variant="h6" sx={{ mt: 2 }}>
              Detalhes do Transporte
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Matrícula"
              name="vehicle_plate"
              value={formData.vehicle_plate}
              onChange={handleChange}
              fullWidth
              error={!!errors.vehicle_plate}
              helperText={errors.vehicle_plate}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Data carga"
              name="load_date"
              type="date"
              value={formData.load_date}
              onChange={handleChange}
              fullWidth
              InputLabelProps={{ shrink: true }}
              error={!!errors.load_date}
              helperText={errors.load_date}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Local de carga"
              name="load_location"
              value={formData.load_location}
              onChange={handleChange}
              fullWidth
              error={!!errors.load_location}
              helperText={errors.load_location}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Endereço de carga"
              name="load_address"
              value={formData.load_address}
              onChange={handleChange}
              fullWidth
              error={!!errors.load_address}
              helperText={errors.load_address}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Cidade de carga"
              name="load_city"
              value={formData.load_city}
              onChange={handleChange}
              fullWidth
              error={!!errors.load_city}
              helperText={errors.load_city}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Caixa Postal de carga"
              name="load_postal_code"
              value={formData.load_postal_code}
              onChange={handleChange}
              fullWidth
              error={!!errors.load_postal_code}
              helperText={errors.load_postal_code}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Local de entrega"
              name="delivery_location"
              value={formData.delivery_location}
              onChange={handleChange}
              fullWidth
              error={!!errors.delivery_location}
              helperText={errors.delivery_location}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Endereço de entrega"
              name="delivery_address"
              value={formData.delivery_address}
              onChange={handleChange}
              fullWidth
              error={!!errors.delivery_address}
              helperText={errors.delivery_address}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Cidade de entrega"
              name="delivery_city"
              value={formData.delivery_city}
              onChange={handleChange}
              fullWidth
              error={!!errors.delivery_city}
              helperText={errors.delivery_city}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              label="Caixa Postal de entrega"
              name="delivery_postal_code"
              value={formData.delivery_postal_code}
              onChange={handleChange}
              fullWidth
              error={!!errors.delivery_postal_code}
              helperText={errors.delivery_postal_code}
            />
          </Grid>
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
              >
                Guardar Guia de Remessa
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
};

export default GuiaRemessa;
