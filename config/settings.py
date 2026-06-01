from pydantic import BaseSettings

class Settings(BaseSettings):
    data_dir: str = "data"
    db_name: str = "metadata.db"
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()