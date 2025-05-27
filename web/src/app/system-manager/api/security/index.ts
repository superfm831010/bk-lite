import useApiClient from '@/utils/request';
import { SystemSettings } from '@/app/system-manager/types/security';

export const useSecurityApi = () => {
  const { get, post, patch } = useApiClient();

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

  /**
   * Get auth sources
   * @returns Promise with auth sources data
   */
  async function getAuthSources(): Promise<any> {
    return await get('/system_mgmt/login_module/');
  }

  /**
   * Update auth source
   * @param id - Auth source ID
   * @param data - Updated auth source data
   * @returns Promise with updated auth source
   */
  async function updateAuthSource(id: number, data: {
    name: string;
    app_id: string;
    app_secret: string;
    other_config: {
      callback_url: string;
      redirect_uri: string;
    };
    enabled: boolean;
  }): Promise<any> {
    return await patch(`/system_mgmt/login_module/${id}/`, data);
  }

  return {
    getSystemSettings,
    updateOtpSettings,
    getAuthSources,
    updateAuthSource
  };
};
