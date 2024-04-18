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

    MAX_TICKERS: int = 10

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

    # Explanation: For example, can't support users wanting to do 5y:5m charts (breaks matplotlib, just too much data)
    # Ensures the user provided combination is valid (also prevents interval > time_frame)
    VALID_CHART_COMBOS: dict = {
        "1d": SUBDAY_INTERVALS,
        "5d": SUBDAY_INTERVALS,
        "1mo": VALID_INTERVALS.copy(),
        "3mo": VALID_INTERVALS.copy(),
        "6mo": VALID_INTERVALS.copy(),
        "ytd": VALID_INTERVALS.copy(),
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

# remove selected intervals
bot_settings.VALID_CHART_COMBOS["1mo"].remove("1m")
bot_settings.VALID_CHART_COMBOS["1mo"].remove("2m")
bot_settings.VALID_CHART_COMBOS["1mo"].remove("1mo")
bot_settings.VALID_CHART_COMBOS["1mo"].remove("3mo")

bot_settings.VALID_CHART_COMBOS["3mo"].remove("1m")
bot_settings.VALID_CHART_COMBOS["3mo"].remove("2m")
bot_settings.VALID_CHART_COMBOS["3mo"].remove("5m")
bot_settings.VALID_CHART_COMBOS["3mo"].remove("15m")
bot_settings.VALID_CHART_COMBOS["3mo"].remove("30m")
bot_settings.VALID_CHART_COMBOS["3mo"].remove("90m")
bot_settings.VALID_CHART_COMBOS["3mo"].remove("3mo")

bot_settings.VALID_CHART_COMBOS["6mo"].remove("1m")
bot_settings.VALID_CHART_COMBOS["6mo"].remove("2m")
bot_settings.VALID_CHART_COMBOS["6mo"].remove("5m")
bot_settings.VALID_CHART_COMBOS["6mo"].remove("15m")
bot_settings.VALID_CHART_COMBOS["6mo"].remove("30m")
bot_settings.VALID_CHART_COMBOS["6mo"].remove("90m")

bot_settings.VALID_CHART_COMBOS["ytd"].remove("1m")
bot_settings.VALID_CHART_COMBOS["ytd"].remove("2m")
bot_settings.VALID_CHART_COMBOS["ytd"].remove("5m")
bot_settings.VALID_CHART_COMBOS["ytd"].remove("15m")
bot_settings.VALID_CHART_COMBOS["ytd"].remove("30m")
bot_settings.VALID_CHART_COMBOS["ytd"].remove("90m")


log = Logger()