"use client";
import { useState } from "react";
import { Input, Button } from "antd";
import { useTranslation } from "@/utils/i18n";

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
  const { t } = useTranslation();
  const [otpCode, setOtpCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleOtpVerification = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!otpCode) {
      onError(t("auth.enterOtpCode"));
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
        onError(responseData.message || t("auth.invalidOtpCode"));
        setIsLoading(false);
      }

    } catch (error) {
      console.error("Error verifying OTP:", error);
      onError(t("auth.otpVerificationFailed"));
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="text-center mb-6">
        <h3 className="text-xl font-semibold text-[var(--color-text-1)]">{t("auth.otpVerification")}</h3>
        <p className="text-[var(--color-text-2)] mt-2">{t("auth.otpVerificationDesc")}</p>
      </div>

      {qrCodeUrl && (
        <div className="mb-6">
          <p className="text-sm text-[var(--color-text-1)] mb-3">{t("auth.installAuthApp")}</p>
          <div className="text-sm text-[var(--color-text-2)] mb-3 pl-4">
            <div>{t("auth.microsoftAuthenticator")}</div>
            <div>{t("auth.freeOtp")}</div>
            <div>{t("auth.googleAuthenticator")}</div>
          </div>
          <p className="text-sm text-[var(--color-text-1)] mb-3">{t("auth.scanQrCode")}</p>
          <div className="flex pl-4">
            <img src={`data:image/png;base64, ${qrCodeUrl}`} alt="QR Code" className="w-48 h-48 border border-gray-300 rounded-lg" />
          </div>
        </div>
      )}

      <form onSubmit={handleOtpVerification} className="flex flex-col space-y-6 w-full">
        <div className="space-y-2">
          <label htmlFor="username-display-otp" className="text-sm font-medium text-[var(--color-text-1)]">{t("auth.username")}</label>
          <Input
            id="username-display-otp"
            type="text"
            value={loginData.username || username}
            className="w-full"
            size="large"
            disabled
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="otp-code" className="text-sm font-medium text-[var(--color-text-1)]">{t("auth.verificationCode")}</label>
          <Input
            id="otp-code"
            type="text"
            placeholder={t("auth.enterVerificationCode")}
            value={otpCode}
            onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
            className="w-full text-center text-lg tracking-wider"
            maxLength={6}
            required
          />
        </div>

        <Button
          type="primary"
          htmlType="submit"
          loading={isLoading}
          className="w-full"
          size="large"
        >
          {isLoading ? t("auth.verifying") : t("auth.verifyCode")}
        </Button>
      </form>
    </div>
  );
}