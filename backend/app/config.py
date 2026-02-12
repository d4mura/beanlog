from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://beanlog:beanlog_dev@localhost:5432/beanlog"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""
    cors_origins: str = "http://localhost:3000"
    embedding_model: str = "all-MiniLM-L6-v2"
    environment: str = "development"
    log_level: str = "DEBUG"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
