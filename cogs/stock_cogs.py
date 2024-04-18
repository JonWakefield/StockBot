import discord
from discord.ext import commands
from src.stocks import Stocks
from config.config import bot_settings, log
from src.exceptions import IntervalError, StockNotFound
from discord.ext.commands import Context

class StockCogs(commands.Cog, 
                name="Stocks",
                description="Commands used to retreive stock based information"):
    
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
            name="Ticker",
            aliases=["ticker"],
            help="Example: !ticker AAPL\nUser can provide multiple tickers in the same request\nExample: !ticker AAPL MSFT NVDA",
            description="Retreive stock based information on the provided Ticker",
            brief="Retreive stock infromation",
            enable=True,
            hidden=False
    )
    async def ticker_command(self, ctx: Context, *tickers: str) -> dict | None:
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
            help="Example: !etf SPY\nUser can provide multiple etfs in the same request\nExample: !etf SPY IWM QQQ",
            description="Retreive ETF information on the provided ETF",
            brief="Retreive ETF infromation",
            enable=True,
            hidden=False
    )
    async def etf_command(self, ctx: Context, *etfs: str) -> dict | None:
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
            name="Coin",
            aliases=["coin"],
            help="Make sure to specify the currency to convert to\nExample: !coin BTC-USD\nUser can provide multiple coins in the same request\nExample: !coin BTC-USD ETH-USD FLOW-USD",
            description="Retreive cryptocurrency information about the provided coin",
            brief="Retreive Cryptocurrency information",
            enalbe=True,
            hidden=False
    )
    async def coin_command(self, ctx: Context, *coins: str) -> dict:

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
            help="Create detailed graphs on the provided ticker\nFormat: !chart [ticker] [chart_type] [time_frame] [interval]\nExample: !chart AAPL\nExample: !chart BTC-USD candle 5d 1h",
            description="Create a chart based on the user provided ticker\n Works on Stocks, ETFs, & Crypto",
            brief="Create Stock Charts",
            enable=True,
            hidden=False
    )
    async def chart_command(self, 
                            ctx: Context, 
                            ticker: str = commands.parameter(default=None, description="Ticker Symbol (EX: AAPL)"), 
                            chart_type: str = commands.parameter(default="line", description="Valid Args: line, candle "), 
                            time_frame: str = commands.parameter(default="ytd", description='Valid Args: {"1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd"}'), 
                            interval: str = commands.parameter(default="1d", description='Valid Args: {"1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"}'), ) -> dict | None:
        """"""
        time_frame = time_frame.lower()
        interval = interval.lower()

        print(ticker)
        print(chart_type)

        if ticker is None:
            await ctx.send("Please provide a ticker. `!help charts` for more details")
            return None

        if time_frame not in bot_settings.VALID_TIME_FRAMES:
            await ctx.send("Please provide a valid time frame `!help charts` for more details")
            return None


        if interval not in bot_settings.VALID_CHART_COMBOS[time_frame]:
            await ctx.send(IntervalError(time_frame, interval))
            return None

        match chart_type.lower():
            case "candle":
                try:
                    chart = await Stocks.create_candle_chart(security=ticker,
                                                         time_frame=time_frame,
                                                         interval=interval)
                except AttributeError as err:
                    await ctx.send(f"Unable to generate a chart for ticker `{ticker.upper()}`. Use `!help chart` for proper formatting")
                    return None
                except StockNotFound as err:
                    print(err)
                    await ctx.send(err)
                    return None
                except Exception as e:
                    log.error(f"Unknown error occured. ticker: {ticker}, time_frame: {time_frame}, interval: {interval}, Error: {e}")
                    await ctx.send(f"Unable to generate a chart for ticker `{ticker.upper()}`. Use `!help chart` for proper formatting")
                    return None

            case "line":
                try:
                    chart = await Stocks.create_line_chart(security=ticker,
                                                        time_frame=time_frame,
                                                        interval=interval)
                except AttributeError as err:
                    await ctx.send(f"Unable to generate a chart for ticker `{ticker.upper()}`. Use `!help chart` for proper formatting")
                    return None
                except StockNotFound as err:
                    print(err)
                    await ctx.send(err)
                    return None
                except Exception as e:
                    log.error(f"Unknown error occured. ticker: {ticker}, time_frame: {time_frame}, interval: {interval}, Error: {e}")
                    await ctx.send(f"Unable to generate a chart for ticker `{ticker.upper()}`. Use `!help chart` for proper formatting")
                    return None
            case _:
                # INVALID CHART chart_type
                print("default")
                await ctx.send("Unrecognized chart type. `!help charts` for more details")
                return None

        # await ctx.send("sending...")
        await ctx.send(file=discord.File(chart, f'chart_{ticker}.jpg'))
