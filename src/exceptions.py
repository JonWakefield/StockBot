from config.config import bot_settings


class IntervalError(Exception):
    """Exception raised for errors in invalid interval time range.

    Attributes:
        message -- explanation of error

    """

    def __init__(self, time_frame: str, interval: str):
        if interval in bot_settings.SUBDAY_INTERVALS:
            self.message = f"Invalid time interval. Request for sub-day data must be within last 30 days."
        else:
            self.message = f"Invalid time interval. Unable to retreive data for provided time range"
        super().__init__(self.message)


class StockNotFound(Exception):
    """Exception raised for unknown ticker symbols.

    Attributes:
        message -- explanation of error

    """

    def __init__(self, ticker: str):
        self.message = f"Unable to retreive stock info for {ticker}"
        super().__init__(self.message)