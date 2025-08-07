'use client';

import { createContext, useContext } from 'react';

export const ModelDetailContext = createContext<any>(null);

export const useModelDetail = () => {
  return useContext(ModelDetailContext);
};
