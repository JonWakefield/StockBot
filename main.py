from config.config import bot_settings, log
import discord
from discord.ext import commands
from cogs.stock_cogs import StockCogs
from src.bot import StockBot

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    stock_bot = StockBot(command_prefix=bot_settings.COMMAND_PREFIX, 
                         intents=intents, 
                         settings=bot_settings)

    @stock_bot.event
    async def on_ready():
        print(stock_bot.user)
        print(stock_bot.user.id)
        await stock_bot.add_cog(StockCogs(stock_bot))
        log.info("stock_bot up and running...")
    

    stock_bot.run(stock_bot.settings.DISCORD_API_SECRET)
 


if __name__ == "__main__":  
    main()
