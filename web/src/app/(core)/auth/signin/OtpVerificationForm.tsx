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

interface OtpVerificationFormProps {
  username: string;
  loginData: LoginResponse;
  qrCodeUrl: string;
  onOtpVerification: (loginData: LoginResponse) => void;
  onError: (error: string) => void;
}

export default function OtpVerificationForm({ 
  username, 
  loginData, 
  qrCodeUrl, 
  onOtpVerification, 
  onError 
}: OtpVerificationFormProps) {
  const [otpCode, setOtpCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleOtpVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!otpCode) {
      onError("Please enter the OTP code");
      return;
    }
    
    setIsLoading(true);
    onError("");
    
    try {
      // Use fetch directly to avoid automatic signIn() call
      const response = await fetch('/api/proxy/core/api/verify_otp_code/', {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify({
          username: loginData.username,
          otp_code: otpCode
        }),
      });
      
      const responseData = await response.json();
      
      if (response.ok && responseData.result) {
        // OTP verification successful, now create NextAuth session
        onOtpVerification(loginData);
      } else {
        onError(responseData.message || "Invalid OTP code");
        setIsLoading(false);
      }
      
    } catch (error) {
      console.error("Error verifying OTP:", error);
      onError("Failed to verify OTP code");
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="text-center mb-6">
        <h3 className="text-xl font-semibold text-gray-800">OTP Verification</h3>
        <p className="text-gray-500 mt-2">Please enter the verification code to complete your login.</p>
      </div>
      
      {qrCodeUrl && (
        <div className="mb-6">
          <p className="text-sm text-gray-600 mb-3">1. Install one of the following apps on your device:</p>
          <div className="text-sm text-gray-500 mb-3 pl-4">
            <div>Microsoft Authenticator</div>
            <div>FreeOTP</div>
            <div>Google Authenticator</div>
          </div>
          <p className="text-sm text-gray-600 mb-3">2. Scan the QR code with your authenticator app:</p>
          <div className="flex pl-4">
            <img src={`data:image/png;base64, ${qrCodeUrl}`} alt="QR Code" className="w-48 h-48 border border-gray-300 rounded-lg" />
          </div>
        </div>
      )}
      
      <form onSubmit={handleOtpVerification} className="flex flex-col space-y-6 w-full">
        <div className="space-y-2">
          <label htmlFor="username-display-otp" className="text-sm font-medium text-gray-700">Username</label>
          <input
            id="username-display-otp"
            type="text"
            value={loginData.username || username}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100"
            disabled
          />
        </div>
        
        <div className="space-y-2">
          <label htmlFor="otp-code" className="text-sm font-medium text-gray-700">Verification Code</label>
          <input
            id="otp-code"
            type="text"
            placeholder="Enter 6-digit code"
            value={otpCode}
            onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out text-center text-lg tracking-wider"
            maxLength={6}
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
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 718-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Verifying...
            </span>
          ) : 'Verify Code'}
        </button>
      </form>
    </div>
  );
}