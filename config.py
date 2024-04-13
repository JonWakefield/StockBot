import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DISCORD_API_SECRET: str = os.getenv('DISCORD_API_TOKEN')




bot_settings = Settings()