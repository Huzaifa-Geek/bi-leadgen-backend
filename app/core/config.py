from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    ENV: str = "development"
    SERPAPI_KEY: str
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
