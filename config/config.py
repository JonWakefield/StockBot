import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from .logger import Logger

load_dotenv()


class Settings(BaseSettings):
    DISCORD_API_SECRET: str = os.getenv('DISCORD_API_TOKEN')




bot_settings = Settings()


log = Logger()