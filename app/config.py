from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    A class for managing application settings using Pydantic's BaseSettings.
    
    This class loads settings from environment variables defined in the .env file.
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """
        Configuration for the Pydantic Settings class.
        """
        env_file = ".env"  # Path to the environment file from which to load variables

# Instantiate the Settings class to access the configuration values
settings = Settings()