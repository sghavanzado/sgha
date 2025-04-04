import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import Dashboard from '../pages/Dashboard';
import NovaFatura from '../pages/NovaFatura';
import NovaFaturaProforma from '../pages/NovaFaturaProforma';
import NovoFornecedor from '../pages/NovoFornecedor';
import NovoCliente from '../pages/NovoCliente';
import NovoProducto from '../pages/NovoProducto';
import Fatura from '../pages/Fatura';
import ClientList from '../pages/ClientList';
import SuppliersList from '../pages/SuppliersList';
import ProductList from '../pages/ProductList';
import UpdateProduct from '../pages/UpdateProduct';
import Unauthorized from '../pages/Unauthorized';
import AuditLog from '../pages/AuditLog';
import UserProfile from '../pages/UserProfile';
import InvoiceManagement from '../pages/InvoiceManagement';
import Settings from '../pages/Settings'; // Import the Settings page
import DataImport from '../pages/DataImport'; // Import DataImport page
import ServicesList from '../pages/ServicesList'; // Import ServicesList page
import NovoServices from '../pages/NovoServices'; // Import NovoServices page

const ContentArea = () => {
  return (
    <Routes>
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/nova-fatura"
        element={
          <ProtectedRoute>
            <NovaFatura />
          </ProtectedRoute>
        }
      />
      <Route
        path="/invoice-management"
        element={
          <ProtectedRoute>
            <InvoiceManagement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/nova-proforma"
        element={
          <ProtectedRoute>
            <NovaFaturaProforma />
          </ProtectedRoute>
        }
      />
      <Route
        path="/novo-cliente"
        element={
          <ProtectedRoute>
            <NovoCliente />
          </ProtectedRoute>
        }
      />
       <Route
        path="/novo-supplier"
        element={
          <ProtectedRoute>
            <NovoFornecedor  />
          </ProtectedRoute>
        }
      />
      <Route
        path="/novo-produto"
        element={
          <ProtectedRoute>
            <NovoProducto />
          </ProtectedRoute>
        }
      />
      <Route
        path="/listagem-produtos"
        element={
          <ProtectedRoute>
            <ProductList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/editar-producto/:id"
        element={
          <ProtectedRoute>
            <UpdateProduct />
          </ProtectedRoute>
        }
      />
      <Route
        path="/clientes"
        element={
          <ProtectedRoute>
            <ClientList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/suppliers"
        element={
          <ProtectedRoute>
            <SuppliersList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/fatura/:id"
        element={
          <ProtectedRoute>
            <Fatura />
          </ProtectedRoute>
        }
      />
      <Route
        path="/perfil"
        element={
          <ProtectedRoute>
            <UserProfile />
          </ProtectedRoute>
        }
      />
      <Route
        path="/auditoria"
        element={
          <ProtectedRoute>
            <AuditLog />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />
      <Route
        path="/import"
        element={
          <ProtectedRoute>
            <DataImport />
          </ProtectedRoute>
        }
      />
      <Route
        path="/services"
        element={
          <ProtectedRoute>
            <ServicesList />
          </ProtectedRoute>
        }
      />
      <Route
        path="/new-service"
        element={
          <ProtectedRoute>
            <NovoServices />
          </ProtectedRoute>
        }
      />
      <Route
        path="/edit-service/:id"
        element={
          <ProtectedRoute>
            <NovoServices />
          </ProtectedRoute>
        }
      />
      <Route path="/nao-autorizado" element={<Unauthorized />} />
      <Route
        path="*"
        element={
          <ProtectedRoute>
            <Navigate to="/dashboard" />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default ContentArea;