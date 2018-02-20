import discord
from discord.ext import commands

class embedthis:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that posts an embeded message"""


        def __init__(self, bot):
                self.bot = bot

		@commands.command(pass_context=True)
        async def embedthis(self, ctx):
                """Let's chat"""


def setup(bot):
        action = embedthis(bot)
        bot.add_cog(action)