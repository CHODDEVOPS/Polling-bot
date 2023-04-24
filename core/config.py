from pydantic import BaseSettings


class BotSettings(BaseSettings):
    token: str

    class Config:
        env_prefix = "BOT_"
        case_sensitive = False


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()


settings = Settings()
