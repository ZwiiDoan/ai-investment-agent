import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Investment Agent API"
    debug: bool = False
    openai_api_key: str = ""
    model: str = "gpt-4o-mini"
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # API Key for authentication
    x_api_key: str = "dev-secret-key"

    # Vector DB credentials (from .env)
    pgvector_db: str = "vectordb"
    pgvector_user: str = "postgres"
    pgvector_password: str = "postgres"
    pgvector_host: str = "localhost"
    pgvector_port: str = "5432"

    # OpenTelemetry / Tracing configuration (override via env vars)
    otel_service_name: str = "ai-investment-agent-backend"
    otlp_http_endpoint: str = "http://localhost:4318/v1/traces"  # For OTLP/HTTP
    otlp_grpc_endpoint: str = "localhost:4317"  # For OTLP/gRPC
    otlp_insecure: bool = True  # For local dev; set False with TLS in production
    otlp_timeout_ms: int = 10000
    otlp_protocol: str = "http"  # or "grpc" if you use gRPC

    # Legacy Jaeger collector override (optional). If set, we can still fall back to JaegerExporter.
    jaeger_collector_endpoint: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    def ensure_otel_env(self):
        # Set correct OTEL endpoint for selected protocol
        if self.otlp_protocol == "grpc":
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = self.otlp_grpc_endpoint
        else:
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = self.otlp_http_endpoint
        os.environ.setdefault("OTEL_SERVICE_NAME", self.otel_service_name)
        os.environ.setdefault("OTEL_EXPORTER_OTLP_INSECURE", str(self.otlp_insecure).lower())
        os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", self.otlp_protocol)


settings = Settings()
settings.ensure_otel_env()
