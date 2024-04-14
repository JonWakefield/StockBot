from config.config import bot_settings, log
import discord
from discord.ext import commands
import yfinance as yf
import matplotlib.pyplot as plt

"""

"""

decimal_places = 2

def add_commas(num: str):
    """ add commas to large numbers to make them more readable """
    new_num = ""
    rev_num = num[::-1]
    if len(num) < 4: return num

    for idx, char in enumerate(rev_num):
        if idx % 3 == 0 and idx != 0:
            new_num = char + "," + new_num
        else:
            new_num = char + new_num

    return new_num

async def get_ticker_info(ticker: str) -> dict:
    """"""
    yf_ticker = yf.Ticker(ticker)

    ticker_info = yf_ticker.info

    try:
        symbol = ticker_info["symbol"]
        fifty_week_low = ticker_info["fiftyTwoWeekLow"] 
        fifty_week_high = ticker_info["fiftyTwoWeekHigh"]
        fifty_day_avg = ticker_info["fiftyDayAverage"]
        short_ratio = ticker_info["shortRatio"]
        company_name = ticker_info["longName"]
        avg_volume = ticker_info["averageVolume"]
    except KeyError as e:
        return {"Status": f"Unable to retreive stock info for {ticker} (For Crypto, use !coin)"}
    
    # TODO: During market hours, See if theres any difference between rec_data_frame data and the recent data from yf_ticker 
    rec_data_frame = yf_ticker.history(period="1d")

    stock_data = {
        "Company": company_name,
        "Ticker": symbol,
        "High": round(rec_data_frame['High'].iloc[0], decimal_places),
        "Open": round(rec_data_frame['Open'].iloc[0], decimal_places),
        "Close": round(rec_data_frame['Close'].iloc[0], decimal_places),
        "Low": round(rec_data_frame['Low'].iloc[0], decimal_places),
        "Volume": add_commas(str(rec_data_frame['Volume'].iloc[0])),
        "Avg. Volume": add_commas(str(avg_volume)),
        "52 Week High": fifty_week_high, 
        "50 Day Avg.": fifty_day_avg,
        "Short Ratio": short_ratio,
        "52 Week Low": fifty_week_low, 
    }

    return stock_data




async def  create_security_chart(security: str,
                                 start: str="2024-04-08",
                                 end: str="2024-04-12"):



    data = yf.download(security, start=start, end=end)
    data['Close'].plot()
    plt.title("Apple Stock Prices")
    plt.show()


async def get_coin_info(coin: str) -> dict:

    coin = coin + "-USD"

    yf_ticker = yf.Ticker(coin)

    coin_info = yf_ticker.info

    try:
        symbol = coin_info["fromCurrency"]
        market = coin_info["lastMarket"]
        fifty_week_low = coin_info["fiftyTwoWeekLow"] 
        fifty_week_high = coin_info["fiftyTwoWeekHigh"]
        fifty_day_avg = coin_info["fiftyDayAverage"]
        avg_volume = coin_info["averageVolume"]
    except KeyError as e:
        return {"Status": f"Unable to retreive coin info for {coin} (For Stocks, use !ticker)"}
    

    # TODO: During market hours, See if theres any difference between rec_data_frame data and the recent data from yf_ticker 
    rec_data_frame = yf_ticker.history(period="1d")


    coin_data = {
        "Market": market,
        "Ticker": symbol,
        "High": round(rec_data_frame['High'].iloc[0], decimal_places),
        "Open": round(rec_data_frame['Open'].iloc[0], decimal_places),
        "Close": round(rec_data_frame['Close'].iloc[0], decimal_places),
        "Low": round(rec_data_frame['Low'].iloc[0], decimal_places),
        "Volume": add_commas(str(rec_data_frame['Volume'].iloc[0])),
        "Avg. Volume": add_commas(str(avg_volume)),
        "52 Week High": fifty_week_high, 
        "50 Day Avg.": fifty_day_avg,
        "52 Week Low": fifty_week_low, 
    }

    return coin_data


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)

    

    log.info("bot up and running...")
    bot.run(bot_settings.DISCORD_API_SECRET)



if __name__ == "__main__":
    main()
