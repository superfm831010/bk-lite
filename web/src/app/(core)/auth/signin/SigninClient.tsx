"use client";
import { signIn } from "next-auth/react";
import { useState } from "react";
import Image from "next/image";

interface SigninClientProps {
  searchParams: {
    callbackUrl: string;
    error: string;
  };
  signinErrors: Record<string | "default", string>;
}

export default function SigninClient({ searchParams: { callbackUrl, error }, signinErrors }: SigninClientProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setFormError("");
    
    const result = await signIn("credentials", {
      redirect: false,
      username,
      password,
      callbackUrl: callbackUrl || "/",
    });
    
    setIsLoading(false);
    
    if (result?.error) {
      setFormError(result.error);
    } else {
      window.location.href = callbackUrl || "/";
    }
  };

  return (
    <div className="flex w-[calc(100%+2rem)] h-screen -m-4">
      <div 
        className="w-3/5 hidden md:block bg-gradient-to-br from-blue-500 to-indigo-700"
        style={{
          backgroundImage: "url('/system-login-bg.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center"
        }}
      >
      </div>
      
      <div className="w-full md:w-2/5 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md">
          <div className="text-center mb-10">
            <div className="flex justify-center mb-6">
              <Image src="/logo-site.png" alt="Logo" width={60} height={60} className="h-14 w-auto" />
            </div>
            <h2 className="text-3xl font-bold text-gray-800">Sign In</h2>
            <p className="text-gray-500 mt-2">Enter your credentials to continue</p>
          </div>
          
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded mb-6">
              <p className="font-medium">{signinErrors[error.toLowerCase()]}</p>
            </div>
          )}
          
          {formError && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded mb-6">
              <p className="font-medium">{formError}</p>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="flex flex-col space-y-6 w-full">
            <div className="space-y-2">
              <label htmlFor="username" className="text-sm font-medium text-gray-700">Username</label>
              <input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
                required
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium text-gray-700">Password</label>
              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
                required
              />
            </div>
            
            <button 
              type="submit" 
              disabled={isLoading}
              className={`w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg shadow transition-all duration-150 ease-in-out transform hover:-translate-y-0.5 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Signing in...
                </span>
              ) : 'Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
