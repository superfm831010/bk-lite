from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    mode: str = 'PROD'
    secret_key: str = ''
    db_uri: str = ''
    admin_password: str = ''

    knowledge_graph_host: str = ''
    knowledge_graph_port: int = 6379
    knowledge_graph_username: str = ''
    knowledge_graph_password: str = ''
    knowledge_graph_database: str = 'default_db'
    
    def is_debug_mode(self) -> bool:
        return self.mode == 'DEBUG'

    def is_prod_mode(self) -> bool:
        return self.mode == 'PROD'

    def graphiti_enabled(self) -> bool:
        return bool(self.knowledge_graph_host and self.knowledge_graph_password)

    class Config:
        env_file = ".env"
        extra = "ignore"


core_settings = CoreSettings()
