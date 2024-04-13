from config import bot_settings
import discord
from discord.ext import commands
import yfinance as yf
import matplotlib.pyplot as plt

"""
    - Retrieve:

        1. Current stock price
        2. Opening price
        3. Closing Price
        4. could do % up / down on the day
        5. Volume
        6. Range ?

        [Full Company Name]
        [QuoteSourceName]

        [Current Price]
        [Opening Price]
        [Closing Price]
        [Volume]
        [Range]

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
    


    # TODO: See if theres any difference between rec_data_frame data and the recent data from yf_ticker 
    rec_data_frame = yf_ticker.history(period="1d")

    open_val = rec_data_frame['Open'].iloc[0]
    high_val = rec_data_frame['High'].iloc[0]

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




async def plot_stock_info(ticker: str, range: str):
    pass
    # data['Close'].plot()
    # plt.title("Apple Stock Prices")
    # plt.show()


async def get_coin_info(coin: str) -> dict:
    pass


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)

    @bot.command(
            help="shown from !help",
            description="This is a description",
            brief="This is a brief",
            enable=True,
            hidden=False,
    )
    async def ping(ctx):
        """ command description (shown when user types !help)"""
        await ctx.send("pong")


    @bot.command(
            aliases=["ticker"],
            description="Retreive stock information on the provided Ticker",
            brief="This is the brief",
            enalbe=True,
            hidden=False
    )
    async def get_stock_info(ctx, ticker: str=None):

        if ticker is None:
            await ctx.send("Please provide a ticker")
            return 
        
        stock_data = await get_ticker_info(ticker=ticker)

        embed = discord.Embed(title="Stock Data", color=0x00ff00)

        for k, v in stock_data.items():
            embed.add_field(name=k, value=v, inline=True)
        
        # to send something back we go 
        await ctx.send(embed=embed)


    bot.run(bot_settings.DISCORD_API_SECRET)



if __name__ == "__main__":
    main()
