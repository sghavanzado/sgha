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
import ProductList from '../pages/ProductList';
import UpdateProduct from '../pages/UpdateProduct';
import Unauthorized from '../pages/Unauthorized';
import AuditLog from '../pages/AuditLog';
import UserProfile from '../pages/UserProfile';

const ContentArea = () => {
  return (
    <Routes>
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      
      <Route path="/nova-fatura" element={
        <ProtectedRoute requiredPermission="create_invoice">
          <NovaFatura />
        </ProtectedRoute>
      } />
      
      <Route path="/nova-proforma" element={
        <ProtectedRoute requiredPermission="create_proforma">
          <NovaFaturaProforma />
        </ProtectedRoute>
      } />
      
      <Route path="/novo-cliente" element={
        <ProtectedRoute requiredPermission="manage_clients">
          <NovoCliente />
        </ProtectedRoute>
      } />
      
      <Route path="/novo-produto" element={
        <ProtectedRoute requiredPermission="manage_products">
          <NovoProducto />
        </ProtectedRoute>
      } />
      
      <Route path="/listagem-produtos" element={
        <ProtectedRoute requiredPermission="view_products">
          <ProductList />
        </ProtectedRoute>
      } />
      
      <Route path="/editar-producto/:id" element={
        <ProtectedRoute requiredPermission="update_products">
          <UpdateProduct />
        </ProtectedRoute>
      } />
      
      <Route path="/clientes" element={
        <ProtectedRoute requiredPermission="view_clients">
          <ClientList />
        </ProtectedRoute>
      } />
      
      <Route path="/novo-fornecedor" element={
        <ProtectedRoute requiredPermission="manage_providers">
          <NovoFornecedor />
        </ProtectedRoute>
      } />
      
      <Route path="/fatura/:id" element={
        <ProtectedRoute requiredPermission="view_invoices">
          <Fatura />
        </ProtectedRoute>
      } />
      
      <Route path="/perfil" element={
        <ProtectedRoute>
          <UserProfile />
        </ProtectedRoute>
      } />
      
      <Route path="/auditoria" element={
        <ProtectedRoute requiredPermission="view_audit_logs">
          <AuditLog />
        </ProtectedRoute>
      } />
      
      <Route path="/nao-autorizado" element={<Unauthorized />} />
      
      <Route path="*" element={
        <ProtectedRoute>
          <Navigate to="/dashboard" />
        </ProtectedRoute>
      } />
    </Routes>
  );
};

export default ContentArea;