import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Fab,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Snackbar,
  CircularProgress,
  Box,
  Alert
} from '@mui/material';
import { Add, Edit, Delete, ErrorOutline } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { Product, productService } from '../api/apiService';

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const data = await productService.getProducts();
        if (Array.isArray(data)) {
          setProducts(data);
        } else {
          setError('Formato de datos inválido recibido del servidor');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error al cargar los productos');
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, []);

  const handleDeleteConfirm = async () => {
    if (!selectedProduct?.id) {
      setError('Producto no válido para eliminar');
      setDeleteDialogOpen(false);
      return;
    }

    try {
      await productService.deleteProduct(selectedProduct.id);
      setProducts(prev => prev.filter(p => p.id !== selectedProduct.id));
      setDeleteDialogOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al eliminar el producto');
      setDeleteDialogOpen(false);
    }
  };

  return (
    <Grid container spacing={3} sx={{ p: { xs: 2, sm: 4 } }}>
      {loading ? (
        <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress size={60} />
        </Grid>
      ) : error ? (
        <Grid item xs={12} sx={{ textAlign: 'center', mt: 4 }}>
          <ErrorOutline color="error" sx={{ fontSize: 60 }} />
          <Typography variant="h6" color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        </Grid>
      ) : (
        products.map(product => (
          <Grid item xs={12} sm={6} md={4} key={product.id}>
            <Card sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              boxShadow: 3,
              borderRadius: 2,
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-4px)',
                boxShadow: 6
              }
            }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                  {product.name}
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    SKU: <strong>{product.sku}</strong>
                  </Typography>
                  <Typography variant="body2">
                    Precio: <strong>${product.price.toFixed(2)}</strong>
                  </Typography>
                  <Typography variant="body2">
                    Stock: <strong>{product.stock} {product.unit}</strong>
                  </Typography>
                  {product.expiration_date && (
                    <Typography variant="body2" color="text.secondary">
                      Vence: {new Date(product.expiration_date).toLocaleDateString()}
                    </Typography>
                  )}
                </Box>

                <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    startIcon={<Edit />}
                    onClick={() => navigate(`/editar-producto/${product.id}`)}
                    aria-label={`Editar ${product.name}`}
                    color="primary"
                  >
                    Editar
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Delete />}
                    onClick={() => {
                      setSelectedProduct(product);
                      setDeleteDialogOpen(true);
                    }}
                    aria-label={`Eliminar ${product.name}`}
                    color="error"
                  >
                    Eliminar
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))
      )}

      <Fab
        color="primary"
        sx={{ 
          position: 'fixed',
          bottom: 32,
          right: 32,
          transition: 'transform 0.2s',
          '&:hover': {
            transform: 'scale(1.1)'
          }
        }}
        onClick={() => navigate('/novo-produto')}
        aria-label="Añadir producto"
      >
        <Add />
      </Fab>

      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle variant="h6" sx={{ fontWeight: 'bold' }}>
          Confirmar eliminación
        </DialogTitle>
        <DialogContent>
          <Typography>
            ¿Estás seguro de eliminar el producto <strong>"{selectedProduct?.name}"</strong> (ID: {selectedProduct?.id})?
          </Typography>
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <Button 
            onClick={() => setDeleteDialogOpen(false)}
            variant="outlined"
            sx={{ mr: 2 }}
          >
            Cancelar
          </Button>
          <Button
            onClick={handleDeleteConfirm}
            variant="contained"
            color="error"
            startIcon={<Delete />}
          >
            Confirmar eliminación
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError('')}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          severity="error" 
          variant="filled"
          sx={{ width: '100%' }}
          onClose={() => setError('')}
        >
          {error}
        </Alert>
      </Snackbar>
    </Grid>
  );
};

export default ProductList;