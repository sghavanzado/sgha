import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import Dashboard from '../pages/Dashboard';
import NovaFatura from '../pages/NovaFatura';
import Recibo from '../pages/Recibo';
import NotaDebito from '../pages/NotaDebito';
import Autofacturacao from '../pages/Autofacturacao';
import FacturaGlobal from '../pages/FacturaGlobal';
import RelatorioFacturacao from '../pages/RelatorioFacturacao';
import FacturacaoPorItem from '../pages/FacturacaoPorItem';
import LiquidacaoImposto from '../pages/LiquidacaoImposto';
import ContaCorrenteCliente from '../pages/ContaCorrenteCliente';
import PagamentosEmFalta from '../pages/PagamentosEmFalta';
import PagamentosEfectuados from '../pages/PagamentosEfectuados';
import MapaImpostos from '../pages/MapaImpostos';
import RelatorioFacturacaoGestores from '../pages/RelatorioFacturacaoGestores';

import GuiaRemessa from '../pages/GuiaRemessa';
import GuiaTransporte from '../pages/GuiaTransporte';
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
        path="/factura-recibo"
        element={
          <ProtectedRoute>
            <Recibo />
          </ProtectedRoute>
        }
      />
      <Route
        path="/nota-debito"
        element={
          <ProtectedRoute>
            <NotaDebito/>
          </ProtectedRoute>
        }
      />
         <Route
        path="/autofacturacao"
        element={
          <ProtectedRoute>
            <Autofacturacao/>
          </ProtectedRoute>
        }
      />
      <Route
        path="/factura-global"
        element={
          <ProtectedRoute>
            <FacturaGlobal />
          </ProtectedRoute>
        }
      />
      <Route
        path="/guia-remessa"
        element={
          <ProtectedRoute>
            <GuiaRemessa />
          </ProtectedRoute>
        }
        />
      <Route
        path="/guia-transporte"
        element={
          <ProtectedRoute>
            <GuiaTransporte />
          </ProtectedRoute>
        }
        />
        
         <Route
        path="/relatorio-facturas"
        element={
          <ProtectedRoute>
            <RelatorioFacturacao />
          </ProtectedRoute>
        }
        />
        <Route
        path="/facturas-item"
        element={
          <ProtectedRoute>
            <FacturacaoPorItem />
          </ProtectedRoute>
        }
        />
        <Route
        path="/liquidacao-impostos"
        element={
          <ProtectedRoute>
            <LiquidacaoImposto />
          </ProtectedRoute>
        }
        />
        <Route
        path="/contas-cliente"
        element={
          <ProtectedRoute>
            <ContaCorrenteCliente/>
          </ProtectedRoute>
        }
        />
        <Route
        path="/pagamentos-falta"
        element={
          <ProtectedRoute>
            <PagamentosEmFalta  />
          </ProtectedRoute>
        }
        />
        <Route
        path="/pagamentos-efectuados"
        element={
          <ProtectedRoute>
            <PagamentosEfectuados />
          </ProtectedRoute>
        }
        />

        <Route
        path="/mapa-impostos"
        element={
          <ProtectedRoute>
            <MapaImpostos />
          </ProtectedRoute>
        }
        />

        <Route
        path="/facturas-gestor"
        element={
          <ProtectedRoute>
            <RelatorioFacturacaoGestores />
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