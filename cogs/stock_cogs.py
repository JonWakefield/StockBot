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
    async def ticker_command(self, ctx, *tickers: str) -> dict:
        # TODO: use *ticker to allow for multiple arguments
        # TODO: Allow user to enter n tickers; if ticker not found, skip it

        if not tickers:
            await ctx.send("Please provide a ticker. `!help ticker` for more details")
            return 
        
        for ticker in tickers:

            stock_data = await Stocks.get_ticker_info(ticker=ticker)
    
            embed = discord.Embed(title=f"Stock Data for ${ticker.upper()}", color=0x00ff00)
    
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
    async def stock_chart_command(self, ctx, stock: str):
        """
            #TODO: Add ability for multiple stocks
            #TODO: Add ability to set time range
            #TODO: Add ability to set what gets plotted (closing price, volume, etc.)
        """
        if stock is None:
            await ctx.send("Please provide a stock. !help for more details")

        stock_chart = await Stocks.create_stock_chart(stock=stock)

