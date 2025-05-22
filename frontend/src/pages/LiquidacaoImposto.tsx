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
  MenuItem,
  Select,
  Alert,
  CircularProgress,
} from '@mui/material';
import { taxSettlementReportService, TaxSettlementRow } from '../api/apiService';
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';

const months = [
  { value: '1', label: 'Janeiro' },
  { value: '2', label: 'Fevereiro' },
  { value: '3', label: 'Março' },
  { value: '4', label: 'Abril' },
  { value: '5', label: 'Maio' },
  { value: '6', label: 'Junho' },
  { value: '7', label: 'Julho' },
  { value: '8', label: 'Agosto' },
  { value: '9', label: 'Setembro' },
  { value: '10', label: 'Outubro' },
  { value: '11', label: 'Novembro' },
  { value: '12', label: 'Dezembro' },
];

const LiquidacaoImposto = () => {
  const [month, setMonth] = useState<string>('5');
  const [year, setYear] = useState<string>('2025');
  const [rows, setRows] = useState<TaxSettlementRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [summary, setSummary] = useState({
    total: 0,
    total_stamp_tax: 0,
  });

  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await taxSettlementReportService.getReport({ month, year });
      setRows(data.rows);
      setSummary(data.summary);
    } catch (err) {
      setError('Erro ao carregar liquidação de impostos');
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

  // Calcular intervalo textual
  const getDateRangeText = () => {
    const m = months.find((x) => x.value === month);
    const y = year;
    if (!m) return '';
    const start = `1 de ${m.label} de ${y}`;
    const end = (() => {
      const d = new Date(Number(y), Number(month), 0);
      return `${d.getDate()} de ${m.label} de ${y}`;
    })();
    return `de ${start} a ${end}`;
  };

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      <Typography variant="h4" gutterBottom>
        Liquidação de Impostos
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        {getDateRangeText()}
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={2}>
            <Select
              value={month}
              onChange={(e) => setMonth(e.target.value as string)}
              fullWidth
              displayEmpty
            >
              {months.map((m) => (
                <MenuItem key={m.value} value={m.value}>
                  {m.label}
                </MenuItem>
              ))}
            </Select>
          </Grid>
          <Grid item xs={12} md={2}>
            <Select
              value={year}
              onChange={(e) => setYear(e.target.value as string)}
              fullWidth
              displayEmpty
            >
              {Array.from({ length: 10 }, (_, i) => {
                const y = 2020 + i;
                return (
                  <MenuItem key={y} value={y.toString()}>
                    {y}
                  </MenuItem>
                );
              })}
            </Select>
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
              <TableCell>Documento</TableCell>
              <TableCell>Total</TableCell>
              <TableCell>Regime de exclusão - Imposto de selo (1,0%)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={3} align="center">
                  <CircularProgress size={32} />
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={3} align="center">
                  Não há dados para apresentar
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row, idx) => (
                <TableRow key={idx}>
                  <TableCell>{row.document}</TableCell>
                  <TableCell>
                    {row.total.toLocaleString('pt-PT', {
                      style: 'currency',
                      currency: 'AOA',
                      minimumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell>
                    {row.stamp_tax.toLocaleString('pt-PT', {
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
              <TableCell align="right">
                <strong>Total</strong>
              </TableCell>
              <TableCell>
                <strong>
                  {summary.total.toLocaleString('pt-PT', {
                    style: 'currency',
                    currency: 'AOA',
                    minimumFractionDigits: 2,
                  })}
                </strong>
              </TableCell>
              <TableCell>
                <strong>
                  {summary.total_stamp_tax.toLocaleString('pt-PT', {
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
    </Box>
  );
};

export default LiquidacaoImposto;
