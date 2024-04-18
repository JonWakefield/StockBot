from discord.ext import commands

class StockBot(commands.Bot):
    
    def __init__(self, command_prefix, intents, settings) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(command_prefix),
            intents=intents,
            help_command=None,
        )

        self.settings = settings

