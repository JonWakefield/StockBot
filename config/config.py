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
    DECIMAL_PLACES: int = 2


    VALID_TIME_FRAMES: set  = {
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    }

    VALID_INTERVALS: set = {
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    }

    VALID_Y_AXIS: set = {
        "Close",
        "Open",
        "High",
        "Low",
        "Volume",
    }



bot_settings = Settings()


log = Logger()