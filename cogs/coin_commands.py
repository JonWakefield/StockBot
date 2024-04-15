import discord
from discord.ext import commands
from src.coins import Coins


class CoinCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
            aliases=["coin"],
            help="This is the help",
            description="Retreive cryptocurrency information about the provided coin",
            brief="This is the brief",
            enalbe=True,
            hidden=False
    )
    async def coin_command(self, ctx, coin: str=None):

        if coin is None:
            await ctx.send("Please provide a coin. !help for more details")
            return
        
        coin_data = await Coins.get_coin_info(coin=coin)

        embed = discord.Embed(title="Coin Data", color=0x00ff00)

        for k, v in coin_data.items():
            embed.add_field(name=k, value=v, inline=True)
        
        # to send something back we go 
        await ctx.send(embed=embed)


    @commands.command(
            aliases=["CoinChart"],
            help="This is the help",
            description="Create a chart for the requested security",
            brief="",
            enable=True,
            hidden=False
    )
    async def coin_chart_command(self, ctx, security: str):
        
        if security is None:
            await ctx.send("Please provide a security. !help for more details")

        # security_chart = await Stocks.create_security_chart(security=security)

