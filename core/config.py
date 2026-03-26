from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_OP_USER: str
    DB_OP_PASSWORD: str
    DB_OP_HOST: str
    DB_OP_PORT: int = 5432
    DB_OP_NAME: str

    DB_ADMIN_USER: str
    DB_ADMIN_PASSWORD: str
    DB_ADMIN_HOST: str
    DB_ADMIN_PORT: int = 5432
    DB_ADMIN_NAME: str
    #jwt
    JWT_EXPIRES_MINUTES: int
    JWT_SECRET: str
    JWT_ALGORITHM: str

    class Config:
        env_file = "develop.env"

settings = Settings()
