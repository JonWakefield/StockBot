from config import bot_settings
import discord
from discord.ext import commands
import yfinance as yf

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


async def get_ticker_info(ticker: str) -> str:
    """"""
    # rec_data = yf.download("AAPL", period="5d")


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
        
        await get_ticker_info(ticker=ticker)
        
        # to send something back we go 
        await ctx.send("Information")


    bot.run(bot_settings.DISCORD_API_SECRET)



if __name__ == "__main__":
    main()
