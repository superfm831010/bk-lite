interface AuthConfig {
  type: string;
  token: string;
  password: string;
  username: string;
  secret_key: string;
}
interface Config {
  url: string;
  params: Record<string, any>;
  auth: AuthConfig;
  method: string;
  headers: Record<string, any>;
  timeout: number;
  content_type: string;
  event_fields_mapping: Record<string, string>;
  event_fields_desc_mapping: Record<string, string>;
}
export interface SourceItem {
  id: number;
  event_count: number | null | undefined | string;
  last_event_time: string;
  created_at: string;
  updated_at: string;
  created_by: string;
  updated_by: string;
  name: string;
  source_id: string;
  source_type: string;
  config: Config;
  secret: string;
  logo: string | null;
  access_type: string;
  is_active: boolean;
  is_effective: boolean;
  description: string;
}
