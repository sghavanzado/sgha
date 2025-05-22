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
  Alert,
  CircularProgress,
} from '@mui/material';
import { billingReportService, BillingReportRow } from '../api/apiService';
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';

const RelatorioFacturacao = () => {
  const [rows, setRows] = useState<BillingReportRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [summary, setSummary] = useState({
    total_subtotal: 0,
    total_tax: 0,
    total_retention: 0,
    total_total: 0,
  });

  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await billingReportService.getReport();
      setRows(data.rows);
      setSummary(data.summary);
    } catch (err) {
      setError('Erro ao carregar relatório de facturação');
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
        Relatório de Facturação
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Listagem de todos os documentos emitidos.
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
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
          <Grid item xs={12} md={10} sx={{ textAlign: { xs: 'left', md: 'right' } }}>
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
                  Não há dados para mostrar
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
            {/* Totals row */}
            <TableRow>
              <TableCell colSpan={4} align="right">
                <strong>Sumário</strong>
              </TableCell>
              <TableCell>
                <strong>
                  {summary.total_subtotal.toLocaleString('pt-PT', {
                    style: 'currency',
                    currency: 'AOA',
                    minimumFractionDigits: 2,
                  })}
                </strong>
              </TableCell>
              <TableCell>
                <strong>
                  {summary.total_retention.toLocaleString('pt-PT', {
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
          <Grid item xs={12} md={3}>
            <Typography>
              Total Incidência:{' '}
              <strong>
                {summary.total_subtotal.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography>
              Imposto/Taxa/IVA:{' '}
              <strong>
                {summary.total_tax.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography>
              Retenção:{' '}
              <strong>
                {summary.total_retention.toLocaleString('pt-PT', {
                  style: 'currency',
                  currency: 'AOA',
                  minimumFractionDigits: 2,
                })}
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
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

export default RelatorioFacturacao;
