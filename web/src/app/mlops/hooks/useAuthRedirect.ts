import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function useAuthRedirect(requireAuth = true) {
  const { status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (requireAuth && status === 'unauthenticated') {
      const currentUrl = encodeURIComponent(window.location.href);
      router.push(`/api/auth/signin?callbackUrl=${currentUrl}`);
    }
  }, [status, requireAuth, router]);

  return {
    status,
    isLoading: status === 'loading',
    isAuthenticated: status === 'authenticated',
  };
}
