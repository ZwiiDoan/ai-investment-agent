from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    app_name: str = "AI Investment Agent API"
    debug: bool = False
    openai_api_key: str = ""
    model: str = "gpt-4o-mini"
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Vector DB credentials (from .env)
    pgvector_db: str = "vectordb"
    pgvector_user: str = "postgres"
    pgvector_password: str = "postgres"
    pgvector_host: str = "localhost"
    pgvector_port: str = "5432"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
