'use client';

import { useSession } from 'next-auth/react';
import { useTranslation } from '@/utils/i18n';
import { createContext, useContext, useEffect, useState } from 'react';
import Spin from '@/components/spin';
import { useLocale } from '@/context/locale';
import { usePathname, useRouter } from 'next/navigation';

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const { data: session, status } = useSession();
  const { t } = useTranslation();
  const { setLocale: changeLocale } = useLocale();
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const authPaths = ['/auth/signin', '/auth/signout'];

  useEffect(() => {
    if (status === 'loading') return;

    const isSessionValid = session?.user && session?.user?.id;
    
    if (!session || !isSessionValid) {
      setToken(null);
      setIsAuthenticated(false);
      
      if (pathname && !authPaths.includes(pathname)) {
        router.push('/auth/signin');
      }
      return;
    }

    if (isSessionValid) {
      setToken(session.user?.id || null);
      setIsAuthenticated(true);
      const userLocale = session.user?.locale || 'en';
      const savedLocale = localStorage.getItem('locale') || 'en';
      if (userLocale !== savedLocale) {
        changeLocale(userLocale);
      }
      localStorage.setItem('locale', userLocale);
    } else {
      console.warn(t('common.noUserSession'));
      if (pathname && !authPaths.includes(pathname)) {
        router.push('/auth/signin');
      }
    }
  }, [status, session, pathname]);

  if (status === 'loading' && pathname && !authPaths.includes(pathname)) {
    return <Spin />;
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export default AuthProvider;
