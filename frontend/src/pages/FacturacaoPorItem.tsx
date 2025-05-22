import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TableContainer,
  MenuItem,
  Select,
  Button,
  InputLabel,
  FormControl,
  Alert,
  CircularProgress,
  TextField,
} from '@mui/material';
import { itemBillingReportService, ItemBillingRow, productService } from '../api/apiService';
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';

const FacturacaoPorItem = () => {
  const [products, setProducts] = useState<any[]>([]);
  const [selectedItem, setSelectedItem] = useState<string>('all');
  const [dateFrom, setDateFrom] = useState<string>('');
  const [dateTo, setDateTo] = useState<string>('');
  const [rows, setRows] = useState<ItemBillingRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [summary, setSummary] = useState({
    total_quantity: 0,
    total_value: 0,
    total_tax: 0,
    total_total: 0,
  });

  useEffect(() => {
    fetchProducts();
    fetchReport();
    // eslint-disable-next-line
  }, []);

  const fetchProducts = async () => {
    try {
      const data = await productService.getProducts();
      setProducts(data);
    } catch (err) {
      setError('Erro ao carregar itens');
    }
  };

  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      const params: any = {};
      if (selectedItem !== 'all') params.item = selectedItem;
      if (dateFrom) params.date_from = dateFrom;
      if (dateTo) params.date_to = dateTo;
      const data = await itemBillingReportService.getReport(params);
      setRows(data.rows);
      setSummary(data.summary);
    } catch (err) {
      setError('Erro ao carregar facturação por item');
    } finally {
      setLoading(false);
    }
  };

  const handleExportExcel = () => {
    alert('Exportação para Excel não implementada nesta demo.');
  };

  const handleDownloadPDF = () => {
    alert('Download em PDF não implementado nesta demo.');
  };

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Typography variant="h4" gutterBottom>
        Facturação por Item
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Valores de {dateFrom ? new Date(dateFrom).toLocaleDateString('pt-PT') : 'sempre'} a {dateTo ? new Date(dateTo).toLocaleDateString('pt-PT') : 'sempre'}
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel id="item-filter-label">Filtrar por itens</InputLabel>
              <Select
                labelId="item-filter-label"
                value={selectedItem}
                label="Filtrar por itens"
                onChange={(e) => setSelectedItem(e.target.value as string)}
              >
                <MenuItem value="all">Todos</MenuItem>
                {products.map((product) => (
                  <MenuItem key={product.sku} value={product.sku}>
                    {product.sku} - {product.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              label="Desde"
              type="date"
              fullWidth
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              label="Até"
              type="date"
              fullWidth
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              variant="contained"
              color="primary"
              onClick={fetchReport}
              sx={{ minWidth: 160 }}
            >
              Atualizar relatório
            </Button>
          </Grid>
          <Grid item xs={12} md={12} sx={{ textAlign: { xs: 'left', md: 'right' } }}>
            <Button
              variant="outlined"
              startIcon={<FileDownloadOutlinedIcon />}
              onClick={handleExportExcel}
              sx={{ mr: 2 }}
            >
              Exportar como Excel
            </Button>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={handleDownloadPDF}
            >
              Download em PDF
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <TableContainer component={Paper} sx={{ mb: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Item</TableCell>
              <TableCell>Descrição</TableCell>
              <TableCell>Quant.</TableCell>
              <TableCell>Preço médio</TableCell>
              <TableCell>Valor</TableCell>
              <TableCell>Imposto</TableCell>
              <TableCell>Total</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <CircularProgress size={32} />
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  Não há dados para apresentar
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row, idx) => (
                <TableRow key={idx}>
                  <TableCell>{row.item}</TableCell>
                  <TableCell>{row.description}</TableCell>
                  <TableCell>{row.quantity}</TableCell>
                  <TableCell>
                    {row.avg_price.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell>
                    {row.value.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell>
                    {row.tax.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell>
                    {row.total.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                </TableRow>
              ))
            )}
            {/* Totals row */}
            <TableRow>
              <TableCell colSpan={2} align="right">
                <strong>Facturado</strong>
              </TableCell>
              <TableCell>
                <strong>{summary.total_quantity}</strong>
              </TableCell>
              <TableCell />
              <TableCell>
                <strong>
                  {summary.total_value.toLocaleString('pt-PT', {
                    style: 'currency',
                    currency: 'AOA',
                    minimumFractionDigits: 2,
                  })}
                </strong>
              </TableCell>
              <TableCell>
                <strong>
                  {summary.total_tax.toLocaleString('pt-PT', {
                    style: 'currency',
                    currency: 'AOA',
                    minimumFractionDigits: 2,
                  })}
                </strong>
              </TableCell>
              <TableCell>
                <strong>
                  {summary.total_total.toLocaleString('pt-PT', {
                    style: 'currency',
                    currency: 'AOA',
                    minimumFractionDigits: 2,
                  })}
                </strong>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      {/* Sumário */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          Sumário
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography>
              Valor:{' '}
              <strong>
                {summary.total_value.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography>
              Imposto:{' '}
              <strong>
                {summary.total_tax.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography>
              Total:{' '}
              <strong>
                {summary.total_total.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default FacturacaoPorItem;
