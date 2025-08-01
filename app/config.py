from pydantic_settings import BaseSettings
from pydantic import Field


# Settings
class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    CORE_DB_NAME: str = Field(..., env="CORE_DB_NAME")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    RABBITMQ_URL: str = Field(..., env="RABBITMQ_URL")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def CORE_DB_URL(self) -> str:
        return f"{self.DATABASE_URL}/{self.CORE_DB_NAME}"

    class Config:
        case_sensitive = True


settings = Settings()
