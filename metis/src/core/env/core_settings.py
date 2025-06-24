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

    neo4j_host: str = ''
    neo4j_username: str = ''
    neo4j_password: str = ''

    mlflow_tracking_uri: str = ''

    def is_debug_mode(self) -> bool:
        return self.mode == 'DEBUG'

    def is_prod_mode(self) -> bool:
        return self.mode == 'PROD'

    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)

    def graphiti_enabled(self) -> bool:
        return bool(self.neo4j_host and self.neo4j_username and self.neo4j_password)

    class Config:
        env_file = ".env"
        extra = "ignore"


core_settings = CoreSettings()
