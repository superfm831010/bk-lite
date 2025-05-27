export interface AuthSource {
  id: number;
  name: string;
  source_type: string;
  app_id: string;
  app_secret: string;
  other_config: {
    callback_url: string;
    redirect_uri: string;
  };
  enabled: boolean;
  is_build_in: boolean;
  icon?: string;
  description?: string;
}

export interface AuthSourceTypeConfig {
  icon: string;
  description: string;
}

export interface SystemSettings {
  enable_otp: string;
  login_expired_time: string;
}