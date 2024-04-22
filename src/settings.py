from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        frozen=True
    )

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    HOST: str = "0.0.0.0"
    PORT: int = 80

    POSTGRES_URL: PostgresDsn


settings = Settings()
async_db_engine = create_async_engine(url=settings.POSTGRES_URL.unicode_string())
async_db_sessionmaker = async_sessionmaker(bind=async_db_engine, expire_on_commit=False)
