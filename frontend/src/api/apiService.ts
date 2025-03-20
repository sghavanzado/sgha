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
  }
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
