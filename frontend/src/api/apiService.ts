// apiService.ts

import axiosInstance from './axiosInstance';

// Interfaces TypeScript
export interface Client {
  id?: number;
  name: string;
  nif: string;
  address: string;
  city: string;
  state: string;
  country: string;
  phone: { phone: string; email: string };
  contact_first_name: string;
  contact_last_name: string;
  contact_email: string;
  contact_phone_number: string;
  payment_terms?: string;
  bank_name?: string;
  iban_number?: string;
}

export interface Supplier {
  id?: number;
  name: string;
  nif: string;
  address: string;
  phone: { phone: string; email: string };
  contact_first_name: string;
  contact_last_name: string;
  contact_email: string;
  contact_phone_number: string;
  payment_terms?: string;
  bank_name?: string;
  iban_number?: string;
}

export interface Invoice {
  id?: number;
  invoice_number: string;
  issue_date: string;
  due_date: string;
  total_amount: number;
  status: 'draft' | 'sent' | 'paid' | 'cancelled';
  client_id: number;
  items: Array<{
    description: string;
    quantity: number;
    unit_price: number;
  }>;
}

export interface Product {
  id?: number;
  sku: string;
  name: string;
  description?: string;
  price: number;
  unit: string;
  category: string;
  expiration_date?: string;
  image_url?: string;
  attributes?: Record<string, unknown>;
  stock: number;
  location?: string;
}

export interface Service {
  id?: number;
  name: string;
  description?: string;
  price: number;
  category: string;
  duration?: string;
  active: boolean;
}

export interface Receipt {
  id?: number;
  receipt_number: string;
  issue_date: string;
  client_id: number;
  total_amount: number;
  client?: any;
}

export interface DebitNote {
  id?: number;
  debit_note_number: string;
  issue_date: string;
  client_id: number;
  total_amount: number;
  client?: any;
}

export interface GlobalInvoice {
  id?: number;
  global_invoice_number: string;
  issue_date: string;
  client_id: number;
  total_amount: number;
  client?: any;
}

export interface SelfBillingReceipt {
  id?: number;
  self_billing_receipt_number: string;
  issue_date: string;
  client_id: number;
  total_amount: number;
  client?: any;
}

export interface ShippingGuide {
  id?: number;
  guide_number: string;
  issue_date: string;
  client_id: number;
  total_amount: number;
  vehicle_plate?: string;
  load_date?: string;
  load_location?: string;
  load_address?: string;
  load_city?: string;
  load_postal_code?: string;
  delivery_location?: string;
  delivery_address?: string;
  delivery_city?: string;
  delivery_postal_code?: string;
  client?: any;
}

export interface OrderNote {
  id?: number;
  order_note_number: string;
  delivery_date: string;
  delivery_location?: string;
  issue_date: string;
  due_date?: string;
  reference?: string;
  series?: string;
  currency?: string;
  notes?: string;
  retention_percent?: number;
  client_id: number;
  items: Array<{
    code: string;
    description: string;
    unit_price: number;
    quantity: number;
    tax_rate: number;
    discount_percent: number;
  }>;
  subtotal: number;
  discount: number;
  taxable_base: number;
  tax: number;
  retention: number;
  total: number;
  client?: any;
}

export interface DeliveryNote {
  id?: number;
  delivery_note_number: string;
  delivery_date: string;
  delivery_location?: string;
  issue_date: string;
  due_date?: string;
  reference?: string;
  series?: string;
  currency?: string;
  notes?: string;
  retention_percent?: number;
  client_id: number;
  items: Array<{
    code: string;
    description: string;
    quantity: number;
    unit_price: number;
    tax_rate: number;
    discount_percent: number;
  }>;
  client?: any;
}

export interface PaymentsMadeRow {
  client_name: string;
  document_type: string;
  receipt_number: string;
  invoice_number: string;
  due_date: string;
  outstanding: number;
  total: number;
}

export interface PaymentsMadeReport {
  rows: PaymentsMadeRow[];
  totals: {
    paid: number;
    due: number;
    not_due: number;
    overdue: number;
    total: number;
  };
}

export interface PaymentsPendingRow {
  client_name: string;
  document_type: string;
  invoice_number: string;
  due_date: string;
  outstanding: number;
  total: number;
}

export interface PaymentsPendingReport {
  rows: PaymentsPendingRow[];
  totals: {
    outstanding: number;
    total: number;
    not_due: number;
    overdue: number;
  };
}

export interface ItemBillingRow {
  item: string;
  description: string;
  quantity: number;
  avg_price: number;
  value: number;
  tax: number;
  total: number;
}

export interface ItemBillingReport {
  rows: ItemBillingRow[];
  summary: {
    total_quantity: number;
    total_value: number;
    total_tax: number;
    total_total: number;
  };
}

export interface TaxMapRow {
  tax_rate: number;
  incidencia: number;
  total_iva: number;
}

export interface TaxMapReport {
  rows: TaxMapRow[];
  total_iva: number;
}

export interface BillingReportRow {
  seller_name: string;
  invoice_number: string;
  client_name: string;
  issue_date: string;
  subtotal: number;
  tax: number;
  retention: number;
  total: number;
}

export interface BillingReport {
  rows: BillingReportRow[];
  summary: {
    total_subtotal: number;
    total_tax: number;
    total_retention: number;
    total_total: number;
  };
}

export interface TaxSettlementRow {
  document: string;
  total: number;
  stamp_tax: number;
}

export interface TaxSettlementReport {
  rows: TaxSettlementRow[];
  summary: {
    total: number;
    total_stamp_tax: number;
  };
}

export interface ClientAccountStatementRow {
  document_type: string;
  document_number: string;
  issue_date: string;
  amount: number;
}

export interface ClientAccountStatementReport {
  rows: ClientAccountStatementRow[];
  client_selected: boolean;
}

// ---------------------Servicio de Productos (Completo)--------------------------
export const productService = {
  createProduct: async (productData: Omit<Product, 'id'>): Promise<Product> => {
    try {
      const response = await axiosInstance.post('/products', productData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear producto');
    }
  },

  getProducts: async (): Promise<Product[]> => {
    try {
      const response = await axiosInstance.get('/products', {
        method: 'GET', // Fuerza método GET
        headers: {
          'X-Requested-With': 'XMLHttpRequest' // Header adicional para evitar OPTIONS
        }
      });
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener productos');
    }
  },

  getProduct: async (id: number): Promise<Product> => {
    try {
      const response = await axiosInstance.get(`/products/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener producto');
    }
  },

  updateProduct: async (id: number, productData: Partial<Product>): Promise<Product> => {
    try {
      const response = await axiosInstance.put(`/products/${id}`, productData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar producto');
    }
  },

  deleteProduct: async (id: number): Promise<void> => {
    try {
      await axiosInstance.delete(`/products/${id}`);
    } catch (error) {
      throw new Error('Error al eliminar producto');
    }
  },

  searchProducts: async (query: string): Promise<Product[]> => {
    try {
      const response = await axiosInstance.get(`/products/search?q=${query}`);
      return response.data;
    } catch (error) {
      throw new Error('Error en la búsqueda de productos');
    }
  }
};

// -----------------Servicio de Clientes-------------------------------------

export const clientService = {
  createClient: async (clientData: Client) => {
    try {
      const response = await axiosInstance.post('/clients', clientData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear cliente');
    }
  },

  getClients: async () => {
    try {
      const response = await axiosInstance.get('/clients');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener clientes');
    }
  },

  updateClient: async (id: number, clientData: Partial<Client>) => {
    try {
      const response = await axiosInstance.put(`/clients/${id}`, clientData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar cliente');
    }
  },

  deleteClient: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/clients/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar cliente');
    }
  }
};

// ---------------- Servicio de Proveedores ---------------------------

export const supplierService = {
  createSupplier: async (supplierData: Supplier) => {
    try {
      const response = await axiosInstance.post('/suppliers', supplierData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear proveedor');
    }
  },

  getSuppliers: async () => {
    try {
      const response = await axiosInstance.get('/suppliers');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener proveedores');
    }
  },

  updateSupplier: async (id: number, supplierData: Partial<Supplier>) => {
    try {
      const response = await axiosInstance.put(`/suppliers/${id}`, supplierData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar proveedor');
    }
  },

  deleteSupplier: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/suppliers/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar proveedor');
    }
  }
};

// --------------- Servicio de Facturas --------------------------
export const invoiceService = {
  createInvoice: async (invoiceData: Invoice) => {
    try {
      const response = await axiosInstance.post('/invoices', invoiceData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear factura');
    }
  },

  getInvoices: async () => {
    try {
      const response = await axiosInstance.get('/invoices');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener facturas');
    }
  },

  getInvoice: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/invoices/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener factura');
    }
  },

  updateInvoice: async (id: number, invoiceData: Partial<Invoice>) => {
    try {
      const response = await axiosInstance.put(`/invoices/${id}`, invoiceData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar factura');
    }
  },

  deleteInvoice: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/invoices/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar factura');
    }
  },

  getNextInvoiceNumber: async (): Promise<{ invoice_number: string }> => {
    try {
      const response = await axiosInstance.get('/invoices/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de factura');
    }
  },

  reserveInvoiceNumber: async (): Promise<{ invoice_number: string }> => {
    try {
      const response = await axiosInstance.post('/invoices/next-number'); // Use POST method
      return response.data;
    } catch (error) {
      throw new Error('Error reserving invoice number');
    }
  },
};

// ----------------- Servicio de Facturas Globales --------------------------
export const globalInvoiceService = {
  createGlobalInvoice: async (globalInvoiceData: GlobalInvoice) => {
    try {
      const response = await axiosInstance.post('/global-invoices', globalInvoiceData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear factura global');
    }
  },

  getGlobalInvoices: async () => {
    try {
      const response = await axiosInstance.get('/global-invoices');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener facturas globales');
    }
  },

  getGlobalInvoice: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/global-invoices/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener factura global');
    }
  },

  updateGlobalInvoice: async (id: number, globalInvoiceData: Partial<GlobalInvoice>) => {
    try {
      const response = await axiosInstance.put(`/global-invoices/${id}`, globalInvoiceData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar factura global');
    }
  },

  deleteGlobalInvoice: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/global-invoices/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar factura global');
    }
  },

  getNextGlobalInvoiceNumber: async (): Promise<{ global_invoice_number: string }> => {
    try {
      const response = await axiosInstance.post('/global-invoices/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de factura global');
    }
  },
};

// ----------------- Servicio de Contabilidad -----------------------
export const accountingService = {
  getAccountPlans: async () => {
    try {
      const response = await axiosInstance.get('/account_plans');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener planes de cuenta');
    }
  },

  getAccountingEntries: async () => {
    try {
      const response = await axiosInstance.get('/accounting_entries');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener asientos contables');
    }
  }
};

// ------------------- Servicio de Usuarios ---------------------------
export const userService = {
  getUsers: async () => {
    try {
      const response = await axiosInstance.get('/users');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener usuarios');
    }
  },

  createUser: async (userData: any) => {
    try {
      const response = await axiosInstance.post('/users', userData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear usuario');
    }
  },

  updateUser: async (userId: number, userData: any) => {
    try {
      const response = await axiosInstance.put(`/users/${userId}`, userData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar usuario');
    }
  },

  deleteUser: async (userId: number) => {
    try {
      const response = await axiosInstance.delete(`/users/${userId}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar usuario');
    }
  }
};

// ------------------- Servicio de Ubicaciones ---------------------------
export const locationService = {
  getCountries: async () => {
    try {
      const response = await axiosInstance.get('/locations/countries');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener países');
    }
  },
  getProvinces: async (countryId: number) => {
    try {
      const response = await axiosInstance.get(`/locations/provinces/${countryId}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener provincias');
    }
  },
};

// ------------------- Servicio de Unidades de Medida ---------------------------
export const unitService = {
  getUnits: async () => {
    try {
      const response = await axiosInstance.get('/units');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener unidades de medida');
    }
  },
};

// ------------------- Servicio de Tipos de Impuestos ---------------------------
export const taxService = {
  getTaxTypes: async () => {
    try {
      const response = await axiosInstance.get('/taxes');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener tipos de impuestos');
    }
  },
  createTaxType: async (taxData: { name: string; rate: number; description?: string }) => {
    try {
      const response = await axiosInstance.post('/taxes', taxData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear tipo de impuesto');
    }
  },
  updateTaxType: async (id: number, taxData: Partial<{ name: string; rate: number; description?: string }>) => {
    try {
      const response = await axiosInstance.put(`/taxes/${id}`, taxData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar tipo de impuesto');
    }
  },
  deleteTaxType: async (id: number) => {
    try {
      await axiosInstance.delete(`/taxes/${id}`);
    } catch (error) {
      throw new Error('Error al eliminar tipo de impuesto');
    }
  },
};

// ------------------- Servicio de Servicios ---------------------------
export const serviceService = {
  createService: async (serviceData: Service) => {
    const response = await axiosInstance.post('/services', serviceData);
    return response.data;
  },
  getServices: async () => {
    const response = await axiosInstance.get('/services');
    return response.data;
  },
  updateService: async (id: number, serviceData: Partial<Service>) => {
    const response = await axiosInstance.put(`/services/${id}`, serviceData);
    return response.data;
  },
  deleteService: async (id: number) => {
    const response = await axiosInstance.delete(`/services/${id}`);
    return response.data;
  },
};

// ------------------- Servicio de Recibos ---------------------------
export const receiptService = {
  createReceipt: async (receiptData: Receipt) => {
    try {
      const response = await axiosInstance.post('/receipts', receiptData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear recibo');
    }
  },

  getReceipts: async () => {
    try {
      const response = await axiosInstance.get('/receipts');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener recibos');
    }
  },

  getReceipt: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/receipts/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener recibo');
    }
  },

  updateReceipt: async (id: number, receiptData: Partial<Receipt>) => {
    try {
      const response = await axiosInstance.put(`/receipts/${id}`, receiptData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar recibo');
    }
  },

  deleteReceipt: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/receipts/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar recibo');
    }
  },

  getNextReceiptNumber: async (): Promise<{ receipt_number: string }> => {
    try {
      const response = await axiosInstance.post('/receipts/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de recibo');
    }
  },
};

// ------------------- Servicio de Notas de Débito ---------------------------
export const debitNoteService = {
  createDebitNote: async (debitNoteData: DebitNote) => {
    try {
      const response = await axiosInstance.post('/debit-notes', debitNoteData);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear nota de débito');
    }
  },

  getDebitNotes: async () => {
    try {
      const response = await axiosInstance.get('/debit-notes');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener notas de débito');
    }
  },

  getDebitNote: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/debit-notes/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener nota de débito');
    }
  },

  updateDebitNote: async (id: number, debitNoteData: Partial<DebitNote>) => {
    try {
      const response = await axiosInstance.put(`/debit-notes/${id}`, debitNoteData);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar nota de débito');
    }
  },

  deleteDebitNote: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/debit-notes/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar nota de débito');
    }
  },

  getNextDebitNoteNumber: async (): Promise<{ debit_note_number: string }> => {
    try {
      const response = await axiosInstance.post('/debit-notes/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de nota de débito');
    }
  },
};

// ------------------- Servicio de Factura-Recibo (Autofacturación) ---------------------------
export const selfBillingReceiptService = {
  createSelfBillingReceipt: async (data: SelfBillingReceipt) => {
    try {
      const response = await axiosInstance.post('/self-billing-receipts', data);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear factura-recibo (autofacturação)');
    }
  },

  getSelfBillingReceipts: async () => {
    try {
      const response = await axiosInstance.get('/self-billing-receipts');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener facturas-recibo (autofacturação)');
    }
  },

  getSelfBillingReceipt: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/self-billing-receipts/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener factura-recibo (autofacturação)');
    }
  },

  updateSelfBillingReceipt: async (id: number, data: Partial<SelfBillingReceipt>) => {
    try {
      const response = await axiosInstance.put(`/self-billing-receipts/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar factura-recibo (autofacturação)');
    }
  },

  deleteSelfBillingReceipt: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/self-billing-receipts/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar factura-recibo (autofacturação)');
    }
  },

  getNextSelfBillingReceiptNumber: async (): Promise<{ self_billing_receipt_number: string }> => {
    try {
      const response = await axiosInstance.post('/self-billing-receipts/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de factura-recibo (autofacturação)');
    }
  },
};

// ----------------- Servicio de Guia de Transporte --------------------------
export const shippingGuideService = {
  createShippingGuide: async (data: ShippingGuide) => {
    try {
      const response = await axiosInstance.post('/shipping-guides', data);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear guía de remessa');
    }
  },

  getShippingGuides: async () => {
    try {
      const response = await axiosInstance.get('/shipping-guides');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener guías de remessa');
    }
  },

  getShippingGuide: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/shipping-guides/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener guía de remessa');
    }
  },

  updateShippingGuide: async (id: number, data: Partial<ShippingGuide>) => {
    try {
      const response = await axiosInstance.put(`/shipping-guides/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar guía de remessa');
    }
  },

  deleteShippingGuide: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/shipping-guides/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar guía de remessa');
    }
  },

  getNextGuideNumber: async (): Promise<{ guide_number: string }> => {
    try {
      const response = await axiosInstance.post('/shipping-guides/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de guía de remessa');
    }
  },
};

// ----------------- Servicio de Notas de Encomenda --------------------------
export const orderNoteService = {
  createOrderNote: async (data: OrderNote) => {
    try {
      const response = await axiosInstance.post('/order-notes', data);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear nota de encomenda');
    }
  },

  getOrderNotes: async () => {
    try {
      const response = await axiosInstance.get('/order-notes');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener notas de encomenda');
    }
  },

  getOrderNote: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/order-notes/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener nota de encomenda');
    }
  },

  updateOrderNote: async (id: number, data: Partial<OrderNote>) => {
    try {
      const response = await axiosInstance.put(`/order-notes/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar nota de encomenda');
    }
  },

  deleteOrderNote: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/order-notes/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar nota de encomenda');
    }
  },

  getNextOrderNoteNumber: async (): Promise<{ order_note_number: string }> => {
    try {
      const response = await axiosInstance.post('/order-notes/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de nota de encomenda');
    }
  },
};

// ----------------- Servicio de Notas de Entrega --------------------------
export const deliveryNoteService = {
  createDeliveryNote: async (data: DeliveryNote) => {
    try {
      const response = await axiosInstance.post('/delivery-notes', data);
      return response.data;
    } catch (error) {
      throw new Error('Error al crear nota de entrega');
    }
  },

  getDeliveryNotes: async () => {
    try {
      const response = await axiosInstance.get('/delivery-notes');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener notas de entrega');
    }
  },

  getDeliveryNote: async (id: number) => {
    try {
      const response = await axiosInstance.get(`/delivery-notes/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener nota de entrega');
    }
  },

  updateDeliveryNote: async (id: number, data: Partial<DeliveryNote>) => {
    try {
      const response = await axiosInstance.put(`/delivery-notes/${id}`, data);
      return response.data;
    } catch (error) {
      throw new Error('Error al actualizar nota de entrega');
    }
  },

  deleteDeliveryNote: async (id: number) => {
    try {
      const response = await axiosInstance.delete(`/delivery-notes/${id}`);
      return response.data;
    } catch (error) {
      throw new Error('Error al eliminar nota de entrega');
    }
  },

  getNextDeliveryNoteNumber: async (): Promise<{ delivery_note_number: string }> => {
    try {
      const response = await axiosInstance.post('/delivery-notes/next-number');
      return response.data;
    } catch (error) {
      throw new Error('Error al obtener el siguiente número de nota de entrega');
    }
  },
};

export const paymentsMadeReportService = {
  getReport: async (params: { client_id?: string; date?: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/payments-made-report?${query}`);
      return response.data as PaymentsMadeReport;
    } catch (error) {
      throw new Error('Erro ao carregar pagamentos efectuados');
    }
  },
};

export const paymentsPendingReportService = {
  getReport: async (params: { client_id?: string; date?: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/payments-pending-report?${query}`);
      return response.data as PaymentsPendingReport;
    } catch (error) {
      throw new Error('Erro ao carregar pagamentos em falta');
    }
  },
};

export const itemBillingReportService = {
  getReport: async (params: { item?: string; date_from?: string; date_to?: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/item-billing-report?${query}`);
      return response.data as ItemBillingReport;
    } catch (error) {
      throw new Error('Erro ao carregar facturação por item');
    }
  },
};

export const taxMapReportService = {
  getReport: async (params: { date_from?: string; date_to?: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/tax-map-report?${query}`);
      return response.data as TaxMapReport;
    } catch (error) {
      throw new Error('Erro ao carregar mapa de impostos');
    }
  },
};

export const billingByEmployeeReportService = {
  getReport: async (params: { date_from?: string; date_to?: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/billing-by-employee-report?${query}`);
      return response.data as BillingByEmployeeReport;
    } catch (error) {
      throw new Error('Erro ao carregar relatório de facturação por colaborador');
    }
  },
};

export const billingReportService = {
  getReport: async () => {
    try {
      const response = await axiosInstance.get(`/billing-report`);
      return response.data as BillingReport;
    } catch (error) {
      throw new Error('Erro ao carregar relatório de facturação');
    }
  },
};

export const taxSettlementReportService = {
  getReport: async (params: { month: string; year: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/tax-settlement-report?${query}`);
      return response.data as TaxSettlementReport;
    } catch (error) {
      throw new Error('Erro ao carregar liquidação de impostos');
    }
  },
};

export const clientAccountStatementReportService = {
  getReport: async (params: { client_id?: string; date_from?: string; date_to?: string }) => {
    try {
      const query = new URLSearchParams(params as any).toString();
      const response = await axiosInstance.get(`/client-account-statement-report?${query}`);
      return response.data as ClientAccountStatementReport;
    } catch (error) {
      throw new Error('Erro ao carregar conta corrente de cliente');
    }
  },
};
