'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { signOut, useSession } from "next-auth/react";
import { clearAuthToken } from '@/utils/crossDomainAuth';

export default function SignoutPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);

  const handleSignout = async () => {
    try {
      setIsLoading(true);
      
      // Call logout API for server-side cleanup
      await fetch("/api/auth/federated-logout", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      // Clear authentication token
      clearAuthToken();
      
      // Use NextAuth's signOut to clear client session
      await signOut({ redirect: false });
      
      // Get callbackUrl parameter and build login page URL
      const callbackUrl = searchParams.get('callbackUrl') || '/';
      const loginUrl = `/auth/signin?callbackUrl=${encodeURIComponent(callbackUrl)}`;
      
      // Redirect to login page
      window.location.href = loginUrl;
    } catch (error) {
      console.error("Logout error:", error);
      // Even if API call fails, still clear token and redirect
      clearAuthToken();
      await signOut({ redirect: false });
      
      const callbackUrl = searchParams.get('callbackUrl') || '/';
      const loginUrl = `/auth/signin?callbackUrl=${encodeURIComponent(callbackUrl)}`;
      window.location.href = loginUrl;
    } finally {
      setIsLoading(false);
    }
  };
  
  if (status === 'loading') {
    return (
      <div className="flex justify-center items-center h-screen">
        Loading...
      </div>
    );
  }

  if (!session) {
    router.push("/api/auth/signin");
    return null;
  }

  return (
    <div className="flex flex-col space-y-3 justify-center items-center h-screen">
      <div className="text-xl font-bold">Signout</div>
      <div>Are you sure you want to sign out?</div>
      <div>
        <button
          onClick={handleSignout}
          disabled={isLoading}
          className="bg-sky-500 hover:bg-sky-700 px-5 py-2 text-sm leading-5 rounded-full font-semibold text-white disabled:opacity-50">
          {isLoading ? "Signing out..." : "Sign out"}
        </button>
      </div>
    </div>
  );
}
