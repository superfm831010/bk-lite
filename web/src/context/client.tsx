import React, { createContext, useContext, useState, useEffect, useCallback, useRef, ReactNode } from 'react';
import useApiClient from '@/utils/request';
import { ClientData } from '@/types/index';

interface ClientDataContextType {
  clientData: ClientData[];
  loading: boolean;
  getAll: () => Promise<ClientData[]>;
  reset: () => void;
  refresh: () => Promise<ClientData[]>;
}

const ClientDataContext = createContext<ClientDataContextType | undefined>(undefined);

export const ClientProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { get, isLoading: apiLoading } = useApiClient();
  const [clientData, setClientData] = useState<ClientData[]>([]);
  const [loading, setLoading] = useState(true);
  const initializedRef = useRef(false);

  const initialize = useCallback(async () => {
    if (initializedRef.current) {
      return;
    }

    if (apiLoading) {
      return;
    }

    try {
      setLoading(true);
      const data = await get('/core/api/get_client/');
      if (data) {
        setClientData(data);
      }
      initializedRef.current = true;
    } catch (err) {
      console.error('Failed to fetch client data:', err);
    } finally {
      setLoading(false);
    }
  }, [get, apiLoading]);

  useEffect(() => {
    initialize();
  }, [initialize]);

  const getAll = useCallback(async () => {
    if (loading || apiLoading) {
      await initialize();
    }
    return [...clientData];
  }, [initialize, loading, apiLoading, clientData]);

  const refresh = useCallback(async () => {
    try {
      const data = await get('/core/api/get_client/');
      if (data) {
        setClientData(data);
      }
      return data || [];
    } catch (err) {
      console.error('Failed to refresh client data:', err);
      return [];
    }
  }, [get]);

  const reset = useCallback(() => {
    setClientData([]);
    setLoading(true);
    initializedRef.current = false;
  }, []);

  return (
    <ClientDataContext.Provider
      value={{ clientData, loading, getAll, reset, refresh }}
    >
      {children}
    </ClientDataContext.Provider>
  );
};

export const useClientData = () => {
  const context = useContext(ClientDataContext);
  if (context === undefined) {
    throw new Error('useClientData must be used within a ClientProvider');
  }
  return context;
};
