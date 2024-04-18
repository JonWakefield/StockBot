import os
import pathlib
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from .logger import Logger

load_dotenv()

class Settings(BaseSettings):

    DISCORD_API_SECRET: str = os.getenv('DISCORD_API_TOKEN')
    DECIMAL_PLACES: int = 2

    COMMAND_PREFIX: str = "!"

    MAX_TICKERS: int = 10

    GREEN_COLOR: str = "#00FF00"
    RED_COLOR: str = "#FF0000"
    VOLUME_COLOR: str = "#00BFFF"
    # BACKGROUND_COLOR: str = "#1B1B1B"
    BACKGROUND_COLOR: str = "#090A11"
    # WHITE_COLOR: str = "#FFFDD0"
    WHITE_COLOR: str = "#EEEEEE"

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

    SUBDAY_INTERVALS: set = {
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d"
    }

    POSTDAY_INTERVALS: set = {
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    }

    DAY_INTERVALS: set = {
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    }

    # Explanation: For example, can't support users wanting to do 5y:5m charts (breaks matplotlib, just too much data, Yfinance doesn't allow it either)
    # Ensures the user provided combination is valid (also prevents interval > time_frame)
    VALID_CHART_COMBOS: dict = {
        "1d": SUBDAY_INTERVALS,
        "5d": SUBDAY_INTERVALS,
        "1mo": {"5m", "15m","30m","60m","90m","1h","1d","5d","1wk"},
        "3mo": {"60m","1h","1d","5d","1wk","1mo"}, # strange enough, yfinance won't let you use 90min intervals, but supports 60min intervals lol
        "6mo": {"60m","1h","1d","5d","1wk","1mo","3mo"},
        "ytd": VALID_INTERVALS, # we will let yfinance manually check this since range varies.
        "1y": POSTDAY_INTERVALS,
        "2y": POSTDAY_INTERVALS,
        "5y": POSTDAY_INTERVALS,
        "10y": POSTDAY_INTERVALS,
    }

    VALID_Y_AXIS: set = {
        "Close",
        "Volume",
    }



bot_settings = Settings()

log = Logger()