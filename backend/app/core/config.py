from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "AI Studio HQ"
    app_env: str = "development"
    secret_key: str = "change-me"
    admin_username: str = "admin"
    admin_password: str = ""
    database_url: str = "sqlite:///./ai_studio.db"
    redis_url: str = "redis://localhost:6379/0"
    vast_api_base: str = "https://cloud.vast.ai/api/v0"
    vast_api_key: str = ""
    vast_provisioning_enabled: bool = False
    vast_max_hourly_price: float = 1.50
    comfyui_base_url: str = "http://localhost:8188"

settings = Settings()
