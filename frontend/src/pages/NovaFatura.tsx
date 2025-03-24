import React, { useState, useEffect } from 'react';
import {
  TextField,
  Button,
  Grid,
  Container,
  Typography,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import axios from 'axios';
import { locationService, unitService, taxService } from '../api/apiService';

const NovaFatura = () => {
  const [formData, setFormData] = useState({
    invoice_number: '',
    issue_date: new Date().toISOString().split('T')[0], // Auto-generated issue date
    seller_id: '',
    seller_name: '',
    client_id: '',
    client_name: '',
    description: '',
    taxable_amount: '',
    vat_rate: '',
    vat_amount: '',
    total_amount: '',
    country: '',
    province: '',
    unit_of_measure: '',
  });

  const [sellers, setSellers] = useState([]); // Ensure sellers is initialized as an array
  const [clients, setClients] = useState([]); // Ensure clients is initialized as an array
  const [products, setProducts] = useState([]);
  const [productDialogOpen, setProductDialogOpen] = useState(false);
  const [productFormData, setProductFormData] = useState({
    product_code: '',
    description: '',
    quantity: '',
    unit_of_measure: '',
    unit_price: '',
    discount: '',
    tax: '',
    total: '',
  });

  const [invoiceItems, setInvoiceItems] = useState([]);
  const [totals, setTotals] = useState({
    total: 0,
    totalTaxes: 0,
    totalDiscounts: 0,
  });

  const [countries, setCountries] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [units, setUnits] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [taxTypes, setTaxTypes] = useState([]);

  useEffect(() => {
    fetchSellers();
    fetchClients();
    generateInvoiceNumber();
    fetchCountries();
    fetchUnits();
    fetchTaxTypes();
  }, []);

  const fetchSellers = async () => {
    try {
      const response = await axios.get('/api/sellers');
      setSellers(Array.isArray(response.data) ? response.data : []); // Ensure response is an array
    } catch (error) {
      console.error('Error fetching sellers:', error);
      setSellers([]); // Fallback to an empty array on error
    }
  };

  const fetchClients = async () => {
    try {
      const response = await axios.get('/api/clients');
      setClients(Array.isArray(response.data) ? response.data : []); // Ensure response is an array
    } catch (error) {
      console.error('Error fetching clients:', error);
      setClients([]); // Fallback to an empty array on error
    }
  };

  const fetchSuppliers = async () => {
    try {
      const response = await axios.get('/suppliers');
      setSuppliers(Array.isArray(response.data) ? response.data : []); // Ensure response is an array
    } catch (error) {
      console.error('Error fetching suppliers:', error);
      setSuppliers([]); // Fallback to an empty array on error
    }
  };

  const generateInvoiceNumber = async () => {
    try {
      const response = await axios.get('/api/invoices/next-number');
      setFormData((prev) => ({
        ...prev,
        invoice_number: response.data.invoice_number,
      }));
    } catch (error) {
      console.error('Error generating invoice number:', error);
    }
  };

  const fetchCountries = async () => {
    try {
      const data = await locationService.getCountries();
      setCountries(data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchProvinces = async (countryId: string) => {
    try {
      const data = await locationService.getProvinces(Number(countryId));
      setProvinces(data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchUnits = async () => {
    try {
      const data = await unitService.getUnits();
      setUnits(data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchTaxTypes = async () => {
    try {
      const data = await taxService.getTaxTypes();
      setTaxTypes(data);
    } catch (error) {
      console.error('Error fetching tax types:', error);
    }
  };

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSellerChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const sellerId = e.target.value;
    const selectedSeller = sellers.find((seller) => seller.id === sellerId);
    if (selectedSeller) {
      setFormData((prev) => ({
        ...prev,
        seller_id: sellerId,
        seller_name: selectedSeller.name,
      }));
    }
  };

  const handleClientChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const clientId = e.target.value;
    const selectedClient = clients.find((client) => client.id === clientId);
    if (selectedClient) {
      setFormData((prev) => ({
        ...prev,
        client_id: clientId,
        client_name: selectedClient.name,
      }));
    }
  };

  const handleProductFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProductFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleAddProduct = () => {
    const newProduct = {
      ...productFormData,
      total:
        (parseFloat(productFormData.quantity) || 0) *
        (parseFloat(productFormData.unit_price) || 0) -
        (parseFloat(productFormData.discount) || 0),
    };
    setInvoiceItems((prev) => [...prev, newProduct]);
    setTotals((prev) => ({
      total: prev.total + newProduct.total,
      totalTaxes: prev.totalTaxes + (parseFloat(productFormData.tax) || 0),
      totalDiscounts: prev.totalDiscounts + (parseFloat(productFormData.discount) || 0),
    }));
    setProductDialogOpen(false);
    setProductFormData({
      product_code: '',
      description: '',
      quantity: '',
      unit_of_measure: '',
      unit_price: '',
      discount: '',
      tax: '',
      total: '',
    });
  };

  const handleCountryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const countryId = e.target.value;
    setSelectedCountry(countryId);
    fetchProvinces(countryId);
    setFormData((prev) => ({ ...prev, country: countryId, province: '' }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/invoices', {
        ...formData,
        items: invoiceItems,
      });
      console.log(response.data);
      // Handle success (e.g., show a success message, clear the form, etc.)
    } catch (error) {
      console.error(error);
      // Handle error (e.g., show an error message)
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Crear Factura
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              name="invoice_number"
              label="Número de Factura"
              fullWidth
              value={formData.invoice_number}
              InputProps={{ readOnly: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="issue_date"
              label="Fecha de Emisión"
              fullWidth
              value={formData.issue_date}
              InputProps={{ readOnly: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              select
              name="seller_id"
              label="Vendedor"
              fullWidth
              value={formData.seller_id}
              onChange={handleSellerChange}
            >
              {sellers.map((seller) => (
                <MenuItem key={seller.id} value={seller.id}>
                  {seller.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              select
              name="client_id"
              label="Cliente"
              fullWidth
              value={formData.client_id}
              onChange={handleClientChange}
            >
              {clients.map((client) => (
                <MenuItem key={client.id} value={client.id}>
                  {client.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField
              name="description"
              label="Descripción"
              fullWidth
              multiline
              rows={4}
              value={formData.description}
              onChange={handleFormChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              select
              label="País"
              fullWidth
              value={formData.country}
              onChange={handleCountryChange}
            >
              {countries.map((country) => (
                <MenuItem key={country.id} value={country.id}>
                  {country.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              select
              label="Provincia"
              fullWidth
              value={formData.province}
              onChange={(e) =>
                setFormData((prev) => ({ ...prev, province: e.target.value }))
              }
              disabled={!selectedCountry}
            >
              {provinces.map((province) => (
                <MenuItem key={province.id} value={province.id}>
                  {province.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
        </Grid>

        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
          Productos
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => setProductDialogOpen(true)}
        >
          Añadir Producto
        </Button>
        <TableContainer component={Paper} sx={{ mt: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Código</TableCell>
                <TableCell>Descripción</TableCell>
                <TableCell>Cantidad</TableCell>
                <TableCell>Unidad</TableCell>
                <TableCell>Precio Unitario</TableCell>
                <TableCell>Descuento</TableCell>
                <TableCell>Impuesto</TableCell>
                <TableCell>Total</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {invoiceItems.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.product_code}</TableCell>
                  <TableCell>{item.description}</TableCell>
                  <TableCell>{item.quantity}</TableCell>
                  <TableCell>{item.unit_of_measure}</TableCell>
                  <TableCell>{item.unit_price}</TableCell>
                  <TableCell>{item.discount}</TableCell>
                  <TableCell>{item.tax}</TableCell>
                  <TableCell>{item.total}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
          Totales
        </Typography>
        <Typography>Total: {totals.total.toFixed(2)}</Typography>
        <Typography>Impuestos: {totals.totalTaxes.toFixed(2)}</Typography>
        <Typography>Descuentos: {totals.totalDiscounts.toFixed(2)}</Typography>

        <Button type="submit" variant="contained" color="primary" sx={{ mt: 4 }}>
          Guardar Factura
        </Button>
      </form>

      {/* Dialog for Adding Products */}
      <Dialog open={productDialogOpen} onClose={() => setProductDialogOpen(false)}>
        <DialogTitle>Añadir Producto</DialogTitle>
        <DialogContent>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                name="product_code"
                label="Código del Producto"
                fullWidth
                value={productFormData.product_code}
                onChange={handleProductFormChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                name="description"
                label="Descripción"
                fullWidth
                value={productFormData.description}
                onChange={handleProductFormChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="quantity"
                label="Cantidad"
                fullWidth
                value={productFormData.quantity}
                onChange={handleProductFormChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="unit_of_measure"
                label="Unidad de Medida"
                fullWidth
                value={productFormData.unit_of_measure}
                onChange={handleProductFormChange}
                select
              >
                {units.map((unit) => (
                  <MenuItem key={unit.id} value={unit.id}>
                    {unit.name} ({unit.abbreviation})
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="unit_price"
                label="Precio Unitario"
                fullWidth
                value={productFormData.unit_price}
                onChange={handleProductFormChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="discount"
                label="Descuento"
                fullWidth
                value={productFormData.discount}
                onChange={handleProductFormChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="tax"
                label="Impuesto"
                fullWidth
                value={productFormData.tax}
                onChange={handleProductFormChange}
                select
              >
                {taxTypes.map((tax) => (
                  <MenuItem key={tax.id} value={tax.rate}>
                    {tax.name} ({tax.rate}%)
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setProductDialogOpen(false)} color="secondary">
            Cancelar
          </Button>
          <Button onClick={handleAddProduct} color="primary">
            Añadir
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default NovaFatura;
