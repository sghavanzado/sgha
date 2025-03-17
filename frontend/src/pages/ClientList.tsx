// components/ClientList.tsx
import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';
import { Client } from '../api/apiService';
import { clientService } from '../api/apiService';
import { Button, Container, Stack, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'name', headerName: 'Nombre', width: 200 },
  { field: 'nif', headerName: 'NIF', width: 130 },
  { field: 'city', headerName: 'Ciudad', width: 130 },
  { field: 'contact_email', headerName: 'Email Contacto', width: 200 },
];

export default function ClientList() {
  const [clients, setClients] = React.useState<Client[]>([]);
  const navigate = useNavigate();

  React.useEffect(() => {
    const fetchClients = async () => {
      try {
        const data = await clientService.getClients();
        setClients(data);
      } catch (error) {
        console.error('Error loading clients:', error);
      }
    };
    fetchClients();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Clientes</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/clients/new')}
        >
          Nuevo Cliente
        </Button>
      </Stack>
      
      <div style={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={clients}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10]}
          onRowClick={(params) => navigate(`/clients/${params.id}`)}
        />
      </div>
    </Container>
  );
}