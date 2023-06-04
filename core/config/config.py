from typing import Any

import json

from pydantic import BaseSettings


class GoogleSettings(BaseSettings):
    application_credentials: str = "google.json"

    @property
    def credentials(self) -> dict[Any, Any]:
        return json.load(open(self.application_credentials))

    class Config:
        env_prefix = "GOOGLE_"
        case_sensitive = False


class BotSettings(BaseSettings):
    token: str

    class Config:
        env_prefix = "BOT_"
        case_sensitive = False


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    firebase: GoogleSettings = GoogleSettings()


settings = Settings()
