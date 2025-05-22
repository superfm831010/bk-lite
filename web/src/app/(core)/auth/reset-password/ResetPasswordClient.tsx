"use client";
import { useState } from "react";
import Image from "next/image";
import useApiClient from '@/utils/request';
import { signIn } from "next-auth/react";

interface ResetPasswordClientProps {
  username: string;
}

export default function ResetPasswordClient({ username }: ResetPasswordClientProps) {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const { post } = useApiClient();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    
    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }
    
    setIsLoading(true);
    setError("");
    
    try {
      await post('/core/api/reset_pwd/', {
        username,
        password: password
      });
      
      setSuccess(true);
      
      // This will automatically get fresh user data from the server
      // where temporary_pwd should now be false after password reset
      await signIn("credentials", {
        username,
        password,
        redirect: false,
      });
      
      setTimeout(() => {
        window.location.href = "/";
      }, 300);
      
    } catch (error) {
      console.error("Error resetting password:", error);
      setError(error instanceof Error ? error.message : "An unknown error occurred");
    } finally {
      setIsLoading(false);
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
            <h2 className="text-3xl font-bold text-gray-800">Reset Password</h2>
            <p className="text-gray-500 mt-2">You are using a temporary password. Please create a new password to continue.</p>
          </div>
          
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded mb-6">
              <p className="font-medium">{error}</p>
            </div>
          )}
          
          {success ? (
            <div className="bg-green-50 border-l-4 border-green-500 text-green-700 p-4 rounded mb-6">
              <p className="font-medium">Password successfully reset! You will be redirected to the home page...</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col space-y-6 w-full">
              <div className="space-y-2">
                <label htmlFor="username" className="text-sm font-medium text-gray-700">Username</label>
                <input
                  id="username"
                  type="text"
                  value={username}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100"
                  disabled
                />
              </div>
              
              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium text-gray-700">New Password</label>
                <input
                  id="password"
                  type="password"
                  placeholder="Enter new password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <label htmlFor="confirmPassword" className="text-sm font-medium text-gray-700">Confirm Password</label>
                <input
                  id="confirmPassword"
                  type="password"
                  placeholder="Confirm new password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
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
                    Resetting Password...
                  </span>
                ) : 'Reset Password'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
