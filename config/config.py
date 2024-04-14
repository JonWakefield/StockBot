import os
import pathlib
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from .logger import Logger

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent
print(f"Base dir is {BASE_DIR}")

CMDS_DIR = BASE_DIR / "cmds"
print(f"CMDS DIR IS {CMDS_DIR}")

class Settings(BaseSettings):
    DISCORD_API_SECRET: str = os.getenv('DISCORD_API_TOKEN')




bot_settings = Settings()


log = Logger()