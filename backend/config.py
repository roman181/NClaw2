from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NCLAW_", env_file=".env", extra="ignore")
    data_dir: Path = Path("./data")
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    @property
    def database_path(self) -> Path:
        return self.data_dir / "nclaw.db"


settings = Settings()
