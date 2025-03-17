import React from 'react';
import { TextField, Button, Typography, Stack, Box } from '@mui/material';

export const ProfileForm: React.FC = () => {
  return (
    <Box 
      component="form"
      sx={{ 
        maxWidth: 600,
        padding: 3,
        borderRadius: 2,
        boxShadow: 1
      }}
    >
      <Typography 
        variant="h4" 
        gutterBottom
        component="h1"
        sx={{ mb: 4 }}
      >
        Perfil de Usuario
      </Typography>
      
      <Stack spacing={3}>
        <TextField
          label="Nombre completo"
          variant="outlined"
          fullWidth
          required
          inputProps={{ 'data-testid': 'fullname-input' }}
        />
        
        <TextField
          label="Correo electrónico"
          type="email"
          fullWidth
          required
          inputProps={{ 
            pattern: "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$",
            'data-testid': 'email-input'
          }}
        />
        
        <TextField
          label="Teléfono"
          type="tel"
          fullWidth
          inputProps={{ 
            pattern: "[0-9]{9}",
            'data-testid': 'phone-input'
          }}
        />
        
        <Button
          type="submit"
          variant="contained"
          size="large"
          sx={{ 
            width: 200,
            mt: 2,
            alignSelf: 'flex-start'
          }}
          aria-label="Guardar cambios del perfil"
        >
          Guardar Cambios
        </Button>
      </Stack>
    </Box>
  );
};