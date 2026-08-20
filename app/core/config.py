from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Cấu hình ứng dụng ---
    APP_DESCRIPTION: str = "Ứng dụng mẫu Authentication & Authorization với FastAPI."
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()