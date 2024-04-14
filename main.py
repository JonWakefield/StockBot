from config.config import bot_settings, log, BASE_DIR, CMDS_DIR
import discord
from discord.ext import commands
from cmds import stock

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

        # load in our python files in the CMDS directory
        for cmd_file in CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

    

    log.info("bot up and running...")
    bot.run(bot_settings.DISCORD_API_SECRET)



if __name__ == "__main__":
    main()
