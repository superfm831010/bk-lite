from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    mode: str = 'PROD'
    secret_key: str = ''
    db_uri: str = ''
    elasticsearch_url: str = ''
    elasticsearch_password: str = ''
    admin_password: str = ''

    supabase_url: str = ''
    supabase_key: str = ''

    def is_debug_mode(self) -> bool:
        return self.mode == 'DEBUG'

    def is_prod_mode(self) -> bool:
        return self.mode == 'PROD'

    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)

    class Config:
        env_file = ".env"
        extra = "ignore"


core_settings = CoreSettings()
