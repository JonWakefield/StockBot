import discord
from discord.ext import commands
from src.coins import Coins


class CoinCogs(commands.Cog, 
               name="Coins",
               description="Commands used to retreive cryptocurrency based information"):
    
    def __init__(self, bot):
        self.bot = bot
    
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
        
        for coin in coins:
            coin_data = await Coins.get_coin_info(coin=coin)
    
            embed = discord.Embed(title=f"Coin Data for ${coin.upper()}", color=0x00ff00)
    
            for k, v in coin_data.items():
                embed.add_field(name=k, value=v, inline=True)
            
            # to send something back we go 
            await ctx.send(embed=embed)
