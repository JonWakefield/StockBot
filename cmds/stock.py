from discord.ext import commands
import yfinance as yf
import matplotlib.pyplot as plt
import discord

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




async def create_security_chart(security: str,
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

@commands.command(
            aliases=["i"],
            help="Get information regarding the bot",
            description="description",
            brief="This is a brief",
            enable=True,
            hidden=False,
)
async def info_command(ctx):
    # TODO: provide some info on stock bot (What he can do, where he gets his data / tickers / coins from )
    str_ = ""


@commands.command(
        aliases=["ticker"],
        help="This is the help",
        description="Retreive stock information on the provided Ticker",
        brief="This is the brief",
        enalbe=True,
        hidden=False
)
async def ticker_command(ctx, ticker: str=None):
    # TODO: use *ticker to allow for multiple arguments
    # TODO: Allow user to enter n tickers; if ticker not found, skip it

    if ticker is None:
        await ctx.send("Please provide a ticker. !help for more details")
        return 
    
    stock_data = await get_ticker_info(ticker=ticker)

    embed = discord.Embed(title="Stock Data", color=0x00ff00)

    for k, v in stock_data.items():
        embed.add_field(name=k, value=v, inline=True)
    
    # to send something back we go 
    await ctx.send(embed=embed)


@commands.command(
        aliases=["coin"],
        help="This is the help",
        description="Retreive cryptocurrency information about the provided coin",
        brief="This is the brief",
        enalbe=True,
        hidden=False
)
async def coin_command(ctx, coin: str=None):

    if coin is None:
        await ctx.send("Please provide a coin. !help for more details")
        return
    
    coin_data = await get_coin_info(coin=coin)

    embed = discord.Embed(title="Coin Data", color=0x00ff00)

    for k, v in coin_data.items():
        embed.add_field(name=k, value=v, inline=True)
    
    # to send something back we go 
    await ctx.send(embed=embed)


@commands.command(
        aliases=["chart"],
        help="This is the help",
        description="Create a chart for the requested security",
        brief="",
        enable=True,
        hidden=False
)
async def ticker_chart_command(ctx, security: str):
    
    if security is None:
        await ctx.send("Please provide a security. !help for more details")

    security_chart = await create_security_chart(security=security)



async def setup(bot):
    bot.add_command(ticker_command)
    bot.add_command(coin_command)
    bot.add_command(ticker_chart_command)
    bot.add_command(info_command)