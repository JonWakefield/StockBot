from discord.ext import commands

@commands.command(
            aliases=["i"],
            help="Get information regarding the bot",
            description="description",
            brief="This is a brief",
            enable=True,
            hidden=False,
)
async def info(ctx):
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