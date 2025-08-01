'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface DocumentsContextType {
  activeTabKey: string;
  setActiveTabKey: (key: string) => void;
  mainTabKey: string;
  setMainTabKey: (key: string) => void;
}

const DocumentsContext = createContext<DocumentsContextType | undefined>(undefined);

export const DocumentsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeTabKey, setActiveTabKey] = useState<string>('file');
  const [mainTabKey, setMainTabKey] = useState<string>('source_files');

  return (
    <DocumentsContext.Provider value={{ 
      activeTabKey, 
      setActiveTabKey, 
      mainTabKey, 
      setMainTabKey 
    }}>
      {children}
    </DocumentsContext.Provider>
  );
};

export const useDocuments = () => {
  const context = useContext(DocumentsContext);
  if (context === undefined) {
    throw new Error('useDocuments must be used within a DocumentsProvider');
  }
  return context;
};