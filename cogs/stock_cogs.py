import discord
from discord.ext import commands
from src.stocks import Stocks
from config.config import bot_settings, log

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
    async def ticker_command(self, ctx, *tickers: str) -> dict | None:
        """"""

        if not tickers:
            await ctx.send("Please provide a ticker. `!help ticker` for more details")
            return None
        
        if len(tickers) > bot_settings.MAX_TICKERS:
            await ctx.send(f"Too many requests sent. Please limit the number of tickers per request to `{bot_settings.MAX_TICKERS}`.")
            return None

        for ticker in tickers:

            try:
                stock_data = await Stocks.get_ticker_info(ticker=ticker)
            except Exception as e:
                log.error(f"Unknown error occured. Details: ticker {ticker}. Error: {e}")
                await ctx.send(f"Error occured retreiving data for {ticker.upper()}. `!help ticker` for more details")
                return None
    
            embed = discord.Embed(title=f"Stock Data for ${ticker.upper()}", color=0x00ff00)
    
            for k, v in stock_data.items():
                embed.add_field(name=k, value=v, inline=True)
            
            # to send something back we go 
            await ctx.send(embed=embed)


    @commands.command(
            name="ETF",
            aliases=["etf"],
            help="Useage Example: !etf SPY\nUser can provide multiple etfs in the same request",
            description="Retreive ETF information on the provided ETF",
            brief="Retreive ETF infromation",
            enable=True,
            hidden=False
    )
    async def etf_command(self, ctx, *etfs: str) -> dict | None:
        if not etfs:
            await ctx.send("Please provide a ETF. `!help etf` for more details")
            return None

        if len(etfs) > bot_settings.MAX_TICKERS:
            await ctx.send(f"Too many requests sent. Please limit the number of tickers per request to `{bot_settings.MAX_TICKERS}`.")
            return None

        for etf in etfs:

            try:
                etf_data = await Stocks.get_etf_info(ticker=etf)
            except Exception as e:
                log.error(f"Unknown error occured. Details: ticker {etf}. Error: {e}")
                await ctx.send(f"Error occured retreiving data for {etf.upper()}. `!help etf` for more details")
                return None
            
            embed = discord.Embed(title=f"ETF data for ${etf.upper()}", color=0x00ff00)

            for k, v in etf_data.items():
                embed.add_field(name=k, value=v, inline=True)

            await ctx.send(embed=embed)


    @commands.command(
            name="Crypto",
            aliases=["coin"],
            help="Useage Example: !coin BTC\nUser can provide multiple coins in the same request",
            description="Retreive cryptocurrency information about the provided coin",
            brief="Retreive Cryptocurrency information",
            enalbe=True,
            hidden=False
    )
    async def coin_command(self, ctx, *coins: str) -> dict:

        if not coins:
            await ctx.send("Please provide a coin. `!help coin` for more details")
            return
        
        if len(coins) > bot_settings.MAX_TICKERS:
            await ctx.send(f"Too many requests sent. Please limit the number of tickers per request to `{bot_settings.MAX_TICKERS}`.")
            return None

        for coin in coins:

            try:
                coin_data = await Stocks.get_coin_info(coin=coin)
            except Exception as e:
                log.error(f"Unknown error occured. Details: ticker {coin}. Error: {e}")
                await ctx.send(f"Error occured retreiving data for {coin.upper()}. `!help coin` for more details")
                return None
    
            embed = discord.Embed(title=f"Coin Data for ${coin.upper()}", color=0x00ff00)
    
            for k, v in coin_data.items():
                embed.add_field(name=k, value=v, inline=True)
            
            # to send something back we go 
            await ctx.send(embed=embed)

    @commands.command(
            name="Chart",
            aliases=["chart"],
            help="Useage Example: !stockchart AAPL\nUser can provide multiple tickers in the same request",
            description="Create a chart based on the user provided ticker",
            brief="Create Stock Charts",
            enable=True,
            hidden=False
    )
    async def chart_command(self, 
                            ctx, 
                            stock: str=None, 
                            chart_type: str="line",
                            time_frame: str="ytd",
                            interval: str="1d") -> dict | None:
        """
        """
        time_frame = time_frame.lower()
        interval = interval.lower()

        if stock is None:
            await ctx.send("Please provide a stock. `!help charts` for more details")
            return None

        if time_frame not in bot_settings.VALID_TIME_FRAMES:
            await ctx.send("Please provide a valid time frame `!help charts` for more details")
            return None


        if interval not in bot_settings.VALID_CHART_COMBOS[time_frame]:
            await ctx.send("Please provide a valid interval `!help charts` for more details")
            return None

        match chart_type:
            case "candle":
                try:
                    chart = await Stocks.create_candle_chart(security=stock,
                                                         time_frame=time_frame,
                                                         interval=interval)
                except AttributeError as err:
                    await ctx.send(f"Unable to generate a chart for ticker `{stock.upper()}`. Use `!help chart` for proper formatting")
                    return None
                except Exception as e:
                    log.error(f"Unknown error occured. ticker: {stock}, time_frame: {time_frame}, interval: {interval}, Error: {e}")
                    await ctx.send(f"Unable to generate a chart for ticker `{stock.upper()}`. Use `!help chart` for proper formatting")
                    return None

            case "line":
                try:
                    chart = await Stocks.create_line_chart(security=stock,
                                                        time_frame=time_frame,
                                                        interval=interval)
                except AttributeError as err:
                    await ctx.send(f"Unable to generate a chart for ticker `{stock.upper()}`. Use `!help chart` for proper formatting")
                    return None
                except Exception as e:
                    log.error(f"Unknown error occured. ticker: {stock}, time_frame: {time_frame}, interval: {interval}, Error: {e}")
                    await ctx.send(f"Unable to generate a chart for ticker `{stock.upper()}`. Use `!help chart` for proper formatting")
                    return None
            case _:
                # INVALID CHART chart_type
                print("default")
                await ctx.send("Unrecognized chart type. `!help charts` for more details")
                return None

        # await ctx.send("sending...")
        await ctx.send(file=discord.File(chart, f'chart_{stock}.jpg'))
