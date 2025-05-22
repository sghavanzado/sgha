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
} from '@mui/material';
import { clientService, paymentsMadeReportService, PaymentsMadeRow } from '../api/apiService';
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';

const PagamentosEfectuados = () => {
  const [clients, setClients] = useState<any[]>([]);
  const [selectedClient, setSelectedClient] = useState<string>('all');
  const [rows, setRows] = useState<PaymentsMadeRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [reportDate, setReportDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [error, setError] = useState('');
  const [totals, setTotals] = useState({
    paid: 0,
    due: 0,
    not_due: 0,
    overdue: 0,
    total: 0,
  });

  useEffect(() => {
    fetchClients();
    fetchReport();
    // eslint-disable-next-line
  }, []);

  const fetchClients = async () => {
    try {
      const data = await clientService.getClients();
      setClients(data);
    } catch (err) {
      setError('Erro ao carregar clientes');
    }
  };

  const fetchReport = async (clientId?: string) => {
    setLoading(true);
    setError('');
    try {
      const data = await paymentsMadeReportService.getReport({
        client_id: clientId || selectedClient,
        date: reportDate,
      });
      setRows(data.rows);
      setTotals(data.totals);
    } catch (err) {
      setError('Erro ao carregar pagamentos efectuados');
    } finally {
      setLoading(false);
    }
  };

  const handleClientChange = (e: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedClient(e.target.value as string);
  };

  const handleUpdateReport = () => {
    fetchReport(selectedClient !== 'all' ? selectedClient : undefined);
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
        Pagamentos Efectuados (Recibos)
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Pagamentos efectuados à data de {new Date(reportDate).toLocaleDateString('pt-PT')}
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel id="client-filter-label">Filtrar por clientes</InputLabel>
              <Select
                labelId="client-filter-label"
                value={selectedClient}
                label="Filtrar por clientes"
                onChange={handleClientChange}
              >
                <MenuItem value="all">Todos</MenuItem>
                {clients.map((client) => (
                  <MenuItem key={client.id} value={client.id}>
                    {client.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpdateReport}
              sx={{ minWidth: 160 }}
            >
              Atualizar relatório
            </Button>
          </Grid>
          <Grid item xs={12} md={6} sx={{ textAlign: { xs: 'left', md: 'right' } }}>
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
              <TableCell>Cliente</TableCell>
              <TableCell>Documento</TableCell>
              <TableCell>Nº de Recibo</TableCell>
              <TableCell>Nº de Factura</TableCell>
              <TableCell>Vence</TableCell>
              <TableCell>Em falta</TableCell>
              <TableCell>Valor</TableCell>
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
                  <TableCell>{row.client_name}</TableCell>
                  <TableCell>{row.document_type}</TableCell>
                  <TableCell>{row.receipt_number}</TableCell>
                  <TableCell>{row.invoice_number}</TableCell>
                  <TableCell>{row.due_date}</TableCell>
                  <TableCell>
                    {row.outstanding.toLocaleString('pt-PT', {
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
              <TableCell colSpan={5} align="right">
                <strong>Total</strong>
              </TableCell>
              <TableCell>
                <strong>
                  {totals.due.toLocaleString('pt-PT', {
                    style: 'currency',
                    currency: 'AOA',
                    minimumFractionDigits: 2,
                  })}
                </strong>
              </TableCell>
              <TableCell>
                <strong>
                  {totals.paid.toLocaleString('pt-PT', {
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
              Não vencido:{' '}
              <strong>
                {totals.not_due.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography>
              Vencido:{' '}
              <strong>
                {totals.overdue.toLocaleString('pt-PT', {
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
                {totals.total.toLocaleString('pt-PT', {
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

export default PagamentosEfectuados;
