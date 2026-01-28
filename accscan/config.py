from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    class Config:
        env_file = ".env"  # Specify the .env file location
        env_file_encoding = 'utf-8'

# Instantiate the settings
settings = Settings() # type:ignore
