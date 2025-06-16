"use client";
import { signIn } from "next-auth/react";
import { useState, useEffect } from "react";
import Image from "next/image";
import PasswordResetForm from "./PasswordResetForm";
import OtpVerificationForm from "./OtpVerificationForm";
import { saveAuthToken } from "@/utils/crossDomainAuth";

interface SigninClientProps {
  searchParams: {
    callbackUrl: string;
    error: string;
  };
  signinErrors: Record<string | "default", string>;
}

type AuthStep = 'login' | 'reset-password' | 'otp-verification';

interface LoginResponse {
  temporary_pwd?: boolean;
  enable_otp?: boolean;
  qrcode?: boolean;
  token?: string;
  username?: string;
  id?: string;
  locale?: string;
}

interface WeChatSettings {
  enabled: boolean;
  app_id?: string;
  app_secret?: string;
  redirect_uri?: string;
}

export default function SigninClient({ searchParams: { callbackUrl, error }, signinErrors }: SigninClientProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isWechatBrowser, setIsWechatBrowser] = useState(false);
  const [authStep, setAuthStep] = useState<AuthStep>('login');
  const [loginData, setLoginData] = useState<LoginResponse>({});
  const [qrCodeUrl, setQrCodeUrl] = useState<string>("");
  const [wechatSettings, setWechatSettings] = useState<WeChatSettings | null>(null);
  const [loadingWechatSettings, setLoadingWechatSettings] = useState(true);

  useEffect(() => {
    const userAgent = navigator.userAgent.toLowerCase();
    setIsWechatBrowser(userAgent.includes('micromessenger') || userAgent.includes('wechat'));
    
    // Fetch WeChat settings
    fetchWechatSettings();
  }, []);

  const fetchWechatSettings = async () => {
    try {
      setLoadingWechatSettings(true);
      const response = await fetch('/api/proxy/core/api/get_wechat_settings/', {
        method: "GET",
        headers: { 
          "Content-Type": "application/json" 
        },
      });
      
      const responseData = await response.json();
      
      if (response.ok && responseData.result) {
        setWechatSettings({
          enabled: true,
          ...responseData.data
        });
      } else {
        setWechatSettings({ enabled: false });
      }
    } catch (error) {
      console.error("Failed to fetch WeChat settings:", error);
      setWechatSettings({ enabled: false });
    } finally {
      setLoadingWechatSettings(false);
    }
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setFormError("");
    
    try {
      const response = await fetch('/api/proxy/core/api/login/', {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });
      
      const responseData = await response.json();
      
      if (!response.ok || !responseData.result) {
        setFormError(responseData.message || "Login failed");
        setIsLoading(false);
        return;
      }
      
      const userData = responseData.data;
      setLoginData(userData);
      
      if (userData.temporary_pwd) {
        setAuthStep('reset-password');
        setIsLoading(false);
        return;
      }
      
      if (userData.enable_otp) {
        if (userData.qrcode) {
          try {
            const qrResponse = await fetch(`/api/proxy/core/api/generate_qr_code/?username=${encodeURIComponent(userData.username)}`, {
              method: "GET",
              headers: { 
                "Content-Type": "application/json" 
              },
            });
            const qrData = await qrResponse.json();
            if (qrResponse.ok && qrData.result) {
              setQrCodeUrl(qrData.data.qr_code);
            }
          } catch (error) {
            console.error("Failed to generate QR code:", error);
          }
        }
        setAuthStep('otp-verification');
        setIsLoading(false);
        return;
      }
      
      await completeAuthentication(userData);
      
    } catch (error) {
      console.error("Login error:", error);
      setFormError("An error occurred during login");
      setIsLoading(false);
    }
  };

  const handlePasswordResetComplete = async (updatedLoginData: LoginResponse) => {
    setLoginData(updatedLoginData);
    
    if (updatedLoginData.enable_otp) {
      if (updatedLoginData.qrcode) {
        try {
          const qrResponse = await fetch(`/api/proxy/core/api/generate_qr_code/?username=${encodeURIComponent(updatedLoginData.username || '')}`, {
            method: "GET",
            headers: { 
              "Content-Type": "application/json" 
            },
          });
          const qrData = await qrResponse.json();
          if (qrResponse.ok && qrData.result) {
            setQrCodeUrl(qrData.data.qr_code || qrData.data.qr_code_url);
          }
        } catch (error) {
          console.error("Failed to generate QR code:", error);
        }
      }
      setAuthStep('otp-verification');
      return;
    }
    
    await completeAuthentication(updatedLoginData);
  };

  const handleOtpVerificationComplete = async (loginData: LoginResponse) => {
    await completeAuthentication(loginData);
  };

  const completeAuthentication = async (userData: LoginResponse) => {
    try {
      const userDataForAuth = {
        id: userData.id || userData.username || 'unknown',
        username: userData.username,
        token: userData.token,
        locale: userData.locale || 'en',
        temporary_pwd: userData.temporary_pwd || false,
        enable_otp: userData.enable_otp || false,
        qrcode: userData.qrcode || false,
      };

      console.log('Completing authentication with user data:', userDataForAuth);

      if (userData.token) {
        saveAuthToken({
          id: userDataForAuth.id,
          username: userDataForAuth.username || '',
          token: userData.token,
          locale: userDataForAuth.locale,
          temporary_pwd: userDataForAuth.temporary_pwd,
          enable_otp: userDataForAuth.enable_otp,
          qrcode: userDataForAuth.qrcode,
        });
      }

      const result = await signIn("credentials", {
        redirect: false,
        username: userDataForAuth.username,
        password: password,
        skipValidation: 'true',
        userData: JSON.stringify(userDataForAuth),
        callbackUrl: callbackUrl || "/",
      });
      
      console.log('SignIn result:', result);
      
      if (result?.error) {
        console.error('SignIn error:', result.error);
        setFormError(result.error);
        setIsLoading(false);
      } else if (result?.ok) {
        console.log('SignIn successful, redirecting to:', callbackUrl || "/");
        window.location.href = callbackUrl || "/";
      } else {
        console.error('SignIn failed with unknown error');
        setFormError("Authentication failed");
        setIsLoading(false);
      }
    } catch (error) {
      console.error("Failed to complete authentication:", error);
      setFormError("Authentication failed");
      setIsLoading(false);
    }
  };

  const handleWechatSignIn = async () => {
    console.log("Starting WeChat login process...");
    console.log("Callback URL:", callbackUrl || "/");
    
    signIn("wechat", { 
      callbackUrl: callbackUrl || "/",
      redirect: true
    });
  };

  const renderLoginForm = () => (
    <form onSubmit={handleLoginSubmit} className="flex flex-col space-y-6 w-full">
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
  );

  const renderPasswordResetForm = () => (
    <PasswordResetForm
      username={username}
      loginData={loginData}
      onPasswordReset={handlePasswordResetComplete}
      onError={setFormError}
    />
  );

  const renderOtpVerificationForm = () => (
    <OtpVerificationForm
      username={username}
      loginData={loginData}
      qrCodeUrl={qrCodeUrl}
      onOtpVerification={handleOtpVerificationComplete}
      onError={setFormError}
    />
  );

  const renderWechatLoginSection = () => {
    if (loadingWechatSettings) {
      return (
        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-gray-50 text-gray-500">Or continue with</span>
            </div>
          </div>
          
          <div className="mt-6">
            <div className="w-full h-12 bg-gray-200 rounded-lg animate-pulse"></div>
          </div>
        </div>
      );
    }

    if (!wechatSettings?.enabled) {
      return null;
    }

    return (
      <div className="mt-6">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-gray-50 text-gray-500">Or continue with</span>
          </div>
        </div>
        
        <div className="mt-6">
          <button
            onClick={handleWechatSignIn}
            className="w-full flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Sign in with WeChat
          </button>
        </div>
        
        {isWechatBrowser && (
          <div className="mt-4 text-center text-sm text-green-600">
            You are using WeChat browser, for best experience use the WeChat login.
          </div>
        )}
      </div>
    );
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
            <h2 className="text-3xl font-bold text-gray-800">
              {authStep === 'login' && 'Sign In'}
              {authStep === 'reset-password' && 'Reset Password'}
              {authStep === 'otp-verification' && 'Verify Identity'}
            </h2>
            <p className="text-gray-500 mt-2">
              {authStep === 'login' && 'Enter your credentials to continue'}
              {authStep === 'reset-password' && 'Create a new password to secure your account'}
              {authStep === 'otp-verification' && 'Complete the verification process'}
            </p>
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
          
          {authStep === 'login' && renderLoginForm()}
          {authStep === 'reset-password' && renderPasswordResetForm()}
          {authStep === 'otp-verification' && renderOtpVerificationForm()}
          
          {authStep === 'login' && renderWechatLoginSection()}
        </div>
      </div>
    </div>
  );
}