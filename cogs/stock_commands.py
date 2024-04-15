import discord
from discord.ext import commands
from src.stocks import Stocks


class StockCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
            aliases=["ticker"],
            help="This is the help",
            description="Retreive stock information on the provided Ticker",
            brief="This is the brief",
            enalbe=True,
            hidden=False
    )
    async def ticker_command(self, ctx, ticker: str=None):
        # TODO: use *ticker to allow for multiple arguments
        # TODO: Allow user to enter n tickers; if ticker not found, skip it

        if ticker is None:
            await ctx.send("Please provide a ticker. !help for more details")
            return 
        
        stock_data = await Stocks.get_ticker_info(ticker=ticker)

        embed = discord.Embed(title="Stock Data", color=0x00ff00)

        for k, v in stock_data.items():
            embed.add_field(name=k, value=v, inline=True)
        
        # to send something back we go 
        await ctx.send(embed=embed)


    @commands.command(
            aliases=["StockChart"],
            help="This is the help",
            description="Create a chart for the requested security",
            brief="",
            enable=True,
            hidden=False
    )
    async def stock_chart_command(self, ctx, security: str):
        
        if security is None:
            await ctx.send("Please provide a security. !help for more details")

        security_chart = await Stocks.create_security_chart(security=security)

