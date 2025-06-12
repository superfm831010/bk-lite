'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter, usePathname } from 'next/navigation';
import { Spin } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { useLocale } from '@/context/locale';

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { data: session, status } = useSession();
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const router = useRouter();
  const pathname = usePathname();
  const { t } = useTranslation();
  const { setLocale } = useLocale();

  const authPaths = ['/auth/signin', '/auth/signout', '/auth/callback'];
  const isSessionValid = session && session.user && session.user.id;

  // Process session changes
  useEffect(() => {
    if (!session || !isSessionValid) {
      setToken(null);
      setIsAuthenticated(false);
      
      if (pathname && !authPaths.includes(pathname)) {
        router.push('/auth/signin');
      }
      return;
    }

    if (isSessionValid) {
      setToken(session.user?.token || session.user?.id || null);
      setIsAuthenticated(true);
      const userLocale = session.user?.locale || 'en';
      const savedLocale = localStorage.getItem('locale') || 'en';
      if (userLocale !== savedLocale) {
        setLocale(userLocale);
      }
      localStorage.setItem('locale', userLocale);
    } else {
      if (pathname && !authPaths.includes(pathname)) {
        router.push('/auth/signin');
      }
    }
  }, [status, session, pathname, setLocale, t]);

  // Show loading state until session state is determined
  if (status === 'loading' && pathname && !authPaths.includes(pathname)) {
    return <Spin />;
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
