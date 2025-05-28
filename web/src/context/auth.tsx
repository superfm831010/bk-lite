'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter, usePathname } from 'next/navigation';
import { Spin } from 'antd';
import { useTranslation } from '@/utils/i18n';
import { useLocale } from '@/context/locale';
import { autoSignInFromSharedAuth } from '@/utils/crossDomainAuth';

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
  const [sharedAuthChecked, setSharedAuthChecked] = useState<boolean>(false);
  const router = useRouter();
  const pathname = usePathname();
  const { t } = useTranslation();
  const { setLocale } = useLocale();

  const authPaths = ['/auth/signin', '/auth/signout', '/auth/callback'];
  const isSessionValid = session && session.user && session.user.id;

  // Check shared authentication state
  useEffect(() => {
    const checkSharedAuth = async () => {
      // If currently on auth-related pages, skip check
      if (pathname && authPaths.includes(pathname)) {
        setSharedAuthChecked(true);
        return;
      }

      // If already have valid session, skip check
      if (status === 'authenticated' && isSessionValid) {
        setSharedAuthChecked(true);
        return;
      }

      // If NextAuth is still loading, wait
      if (status === 'loading') {
        return;
      }

      try {
        // Try auto sign-in from shared authentication state
        const autoSignInSuccess = await autoSignInFromSharedAuth();
        if (autoSignInSuccess) {
          // Auto sign-in successful, wait for session update
          console.log('Auto sign-in from shared auth successful');
          return;
        }
      } catch (error) {
        console.error('Error checking shared auth:', error);
      } finally {
        setSharedAuthChecked(true);
      }
    };

    checkSharedAuth();
  }, [status, pathname, isSessionValid]);

  // Only process session after shared authentication check is complete
  useEffect(() => {
    if (!sharedAuthChecked) {
      return;
    }

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
      console.warn(t('common.noUserSession'));
      if (pathname && !authPaths.includes(pathname)) {
        router.push('/auth/signin');
      }
    }
  }, [status, session, pathname, sharedAuthChecked, setLocale, t]);

  // Show loading state until shared authentication check is complete and session state is determined
  if (!sharedAuthChecked || (status === 'loading' && pathname && !authPaths.includes(pathname))) {
    return <Spin />;
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
