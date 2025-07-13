from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Finance App"
    default_file_path: str = "data/operations.xlsx"

settings = Settings()