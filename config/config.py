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

    GREEN_COLOR: str = "#00FF00"
    RED_COLOR: str = "#FF0000"
    VOLUME_COLOR: str = "#00BFFF"
    BACKGROUND_COLOR: str = "#1B1B1B"
    WHITE_COLOR: str = "#FFFDD0"

    CANDLE_WIDTH: float = 0.9
    STEM_WIDTH: float = 0.4

    FONT_DICT: dict = {
            'family': 'serif',
            'color': WHITE_COLOR,
            'weight': 'bold',
            'size': 16,
    }
    

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
    }

    # not used but leaving as reference for all possible invtervals yfinance supports
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

    SUBDAY_RANGES: set = {
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
    }

    DAY_RANGES: set = {
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    }

    # Explanation: For example, can't support users wanting to do 5y:5m charts (breaks matplotlib, just too much data)
    # Ensures the user provided combination is valid (also prevents interval > time_frame)
    VALID_CHART_COMBOS: dict = {
        "1d": SUBDAY_RANGES,
        "5d": SUBDAY_RANGES.add("1d"),
        "1mo": VALID_INTERVALS.remove("3mo"),
        "3mo": VALID_INTERVALS,
        "6mo": VALID_INTERVALS,
        "1y": VALID_INTERVALS,
        "2y": VALID_INTERVALS,
        "5y": VALID_INTERVALS,
        "10y": VALID_INTERVALS,
        "ytd": VALID_INTERVALS,
    }

    VALID_Y_AXIS: set = {
        "Close",
        "Volume",
    }



bot_settings = Settings()


log = Logger()