import discord
from discord.ext import commands
from src.stocks import Stocks


class StockCogs(commands.Cog, 
                name="Stocks",
                description="Commands used to retreive stock based information"):
    
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
            name="Ticker",
            aliases=["ticker"],
            help="Useage Example: !ticker AAPL\nUser can provide multiple tickers in the same request",
            description="Retreive stock based information on the provided Ticker",
            brief="Retreive stock infromation",
            enable=True,
            hidden=False
    )
    async def ticker_command(self, ctx, *ticker: str):
        # TODO: use *ticker to allow for multiple arguments
        # TODO: Allow user to enter n tickers; if ticker not found, skip it
        print(ticker)
        print(type(ticker))
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
            name="StockCharts",
            aliases=["stockchart"],
            help="Useage Example: !stockchart AAPL\nUser can provide multiple tickers in the same request",
            description="Create a chart based on the user provided ticker",
            brief="Create Stock Charts",
            enable=True,
            hidden=False
    )
    async def stock_chart_command(self, ctx, security: str):
        """
            #TODO: Add ability for multiple stocks
            #TODO: Add ability to set time range
            #TODO: Add ability to set what gets plotted (closing price, volume, etc.)
        """
        if security is None:
            await ctx.send("Please provide a security. !help for more details")

        security_chart = await Stocks.create_security_chart(security=security)

