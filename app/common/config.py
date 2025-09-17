from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / '.env'

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=ENV_PATH)

settings = Settings()

if __name__ == "__main__":
    print(f"Host: {settings.DB_HOST}")
    print(f"Port: {settings.DB_PORT}")
    print(f"User: {settings.DB_USER}")
    print(f"Database: {settings.DB_NAME}")
    print(f"URL: {settings.DATABASE_URL}")