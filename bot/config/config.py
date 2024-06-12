from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    AUTO_CLAIM: bool = True
    AUTO_UPGRADE: bool = True
    AUTO_BUY: bool = False
    AUTO_BATTLE: bool = False
    DELAY_BETWEEN_BATTLES: list[int] = [5, 10]
    CLICK_COOLDOWN: list[float] = [0.085, 0.09]
    BATTLES_COUNT: int = 10
   
    USE_PROXY_FROM_FILE: bool = False


settings = Settings()


