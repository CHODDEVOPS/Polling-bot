from typing import Any

import json

from loguru import logger
from pydantic import BaseSettings


class GoogleSettings(BaseSettings):
    application_credentials: str = "google.json"

    @property
    def credentials(self) -> dict[Any, Any]:
        try:
            return json.load(open(self.application_credentials))
        except FileNotFoundError as exc:
            msg = (
                "Google credentials file `%s` was not found. Please, put it into the project root"
                % self.application_credentials
            )
            logger.error(msg)
            raise ValueError(msg) from exc

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
