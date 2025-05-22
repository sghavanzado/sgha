import React, { useState } from 'react';
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
  Button,
  TextField,
  Alert,
  CircularProgress,
} from '@mui/material';
import { billingByEmployeeReportService, BillingByEmployeeRow } from '../api/apiService';
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';

const RelatorioFacturacaoGestores= () => {
  const [dateFrom, setDateFrom] = useState<string>('');
  const [dateTo, setDateTo] = useState<string>('');
  const [rows, setRows] = useState<BillingByEmployeeRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      const params: any = {};
      if (dateFrom) params.date_from = dateFrom;
      if (dateTo) params.date_to = dateTo;
      const data = await billingByEmployeeReportService.getReport(params);
      setRows(data.rows);
    } catch (err) {
      setError('Erro ao carregar relatório de facturação por colaborador');
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
        Relatório de Facturação por colaborador
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Listagem de todos os documentos emitidos por colaborador.
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
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
          <Grid item xs={12} md={4} sx={{ textAlign: { xs: 'left', md: 'right' } }}>
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
              <TableCell>Documento</TableCell>
              <TableCell>Número</TableCell>
              <TableCell>Cliente</TableCell>
              <TableCell>Data</TableCell>
              <TableCell>S/Taxa/IVA</TableCell>
              <TableCell>Retenção</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <CircularProgress size={32} />
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  Não há dados para apresentar
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row, idx) => (
                <TableRow key={idx}>
                  <TableCell>{row.seller_name}</TableCell>
                  <TableCell>{row.invoice_number}</TableCell>
                  <TableCell>{row.client_name}</TableCell>
                  <TableCell>{row.issue_date ? new Date(row.issue_date).toLocaleDateString('pt-PT') : ''}</TableCell>
                  <TableCell>
                    {row.subtotal.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell>
                    {row.retention.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default RelatorioFacturacaoGestores;
