'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signOut, useSession } from "next-auth/react";

export default function SignoutPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSignout = async () => {
    try {
      setIsLoading(true);
      // Simple API call to the logout endpoint to handle any server-side cleanup
      await fetch("/api/auth/federated-logout", {
        method: "POST",
      });
      
      // Use NextAuth's signOut to clear the client session
      await signOut({ redirect: false });
      
      // Redirect to home page after successful logout
      router.push("/");
    } catch (error) {
      console.error("Logout error:", error);
      // Still try to sign out even if the API call fails
      await signOut({ redirect: false });
      router.push("/");
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
