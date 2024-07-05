from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    app_name: str = "My App"
    log_level: str
    mongo_uri: str
    mongo_db: str
    api_key_length: int
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiration: int

settings = Settings()