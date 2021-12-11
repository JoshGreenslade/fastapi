from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_usr: str
    db_pwd: str
    auth_secret_key: str
    auth_algorithm: str
    auth_expire_time_min: int

    class Config:
        env_file = ".env"


settings = Settings()
