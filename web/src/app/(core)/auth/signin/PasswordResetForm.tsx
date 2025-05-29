"use client";
import { useState } from "react";

interface LoginResponse {
  temporary_pwd?: boolean;
  enable_otp?: boolean;
  qrcode?: boolean;
  token?: string;
  username?: string;
  id?: string;
  locale?: string;
}

interface PasswordResetFormProps {
  username: string;
  loginData: LoginResponse;
  onPasswordReset: (updatedLoginData: LoginResponse) => void;
  onError: (error: string) => void;
}

export default function PasswordResetForm({ 
  username, 
  loginData, 
  onPasswordReset, 
  onError 
}: PasswordResetFormProps) {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handlePasswordReset = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (newPassword !== confirmPassword) {
      onError("Passwords do not match");
      return;
    }
    
    if (newPassword.length < 8) {
      onError("Password must be at least 8 characters long");
      return;
    }
    
    setIsLoading(true);
    onError("");
    
    try {
      const response = await fetch('/api/proxy/core/api/reset_pwd/', {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify({
          username: loginData.username,
          password: newPassword
        }),
      });
      
      const responseData = await response.json();
      
      if (!response.ok || !responseData.result) {
        onError(responseData.message || "Password reset failed");
        setIsLoading(false);
        return;
      }
      
      // Update login data to remove temporary_pwd flag
      const updatedLoginData = { ...loginData, temporary_pwd: false };
      onPasswordReset(updatedLoginData);
      
    } catch (error) {
      console.error("Error resetting password:", error);
      onError(error instanceof Error ? error.message : "An unknown error occurred");
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="text-center mb-6">
        <h3 className="text-xl font-semibold text-gray-800">Reset Password</h3>
        <p className="text-gray-500 mt-2">You are using a temporary password. Please create a new password to continue.</p>
      </div>
      
      <form onSubmit={handlePasswordReset} className="flex flex-col space-y-6 w-full">
        <div className="space-y-2">
          <label htmlFor="username-display" className="text-sm font-medium text-gray-700">Username</label>
          <input
            id="username-display"
            type="text"
            value={loginData.username || username}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100"
            disabled
          />
        </div>
        
        <div className="space-y-2">
          <label htmlFor="new-password" className="text-sm font-medium text-gray-700">New Password</label>
          <input
            id="new-password"
            type="password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
            required
          />
        </div>
        
        <div className="space-y-2">
          <label htmlFor="confirm-password" className="text-sm font-medium text-gray-700">Confirm Password</label>
          <input
            id="confirm-password"
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
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Resetting Password...
            </span>
          ) : 'Reset Password'}
        </button>
      </form>
    </div>
  );
}