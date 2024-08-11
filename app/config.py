from pydantic_settings import BaseSettings, SettingsConfigDict
import os

if "tests" in os.listdir(os.getcwd()):  # bgr-admin-backend directory
    ENV = "dev"
else:
    ENV = "prod"


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int

    model_config = SettingsConfigDict(env_file=f"./app/.env.{ENV}")


settings = Settings()
