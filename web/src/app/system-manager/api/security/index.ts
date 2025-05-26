import useApiClient from '@/utils/request';

export interface SystemSettings {
  enable_otp: string;
  login_expired_time: string;
}

export const useSecurityApi = () => {
  const { get, post } = useApiClient();

  /**
   * Get system settings including OTP status
   * @returns Promise with system settings data
   */
  async function getSystemSettings(): Promise<SystemSettings> {
    return await get('/system_mgmt/system_settings/get_sys_set/');
  }

  /**
   * Update OTP settings
   * @param enableOtp - "1" to enable OTP, "0" to disable
   * @returns Promise with updated settings
   */
  async function updateOtpSettings({ enableOtp, loginExpiredTime }: { enableOtp: string; loginExpiredTime: string }): Promise<any> {
    return await post('/system_mgmt/system_settings/update_sys_set/', {
      enable_otp: enableOtp,
      login_expired_time: loginExpiredTime
    });
  }

  return {
    getSystemSettings,
    updateOtpSettings
  };
};
