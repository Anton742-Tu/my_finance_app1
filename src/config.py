from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:pass@localhost:5432/finance"
    secret_key: str = "your-secret-key"

    class Config:
        env_file = ".env"


settings = Settings()
