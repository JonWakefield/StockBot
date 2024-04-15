from config.config import bot_settings, log
import discord
from discord.ext import commands
from cogs.coin_cogs import CoinCogs
from cogs.stock_cogs import StockCogs
"""

"""

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)

        await bot.add_cog(StockCogs(bot))
        await bot.add_cog(CoinCogs(bot))

    

    log.info("bot up and running...")
    bot.run(bot_settings.DISCORD_API_SECRET)
 


if __name__ == "__main__":  
    main()
