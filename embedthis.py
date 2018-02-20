import discord
from discord.ext import commands

class embedthis:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that posts an embeded message"""


        def __init__(self, bot):
                self.bot = bot

		@commands.command(pass_context=True)
        async def embedthis(self, ctx):
                """Let's chat"""
# maybe do this from importing an attachment and embedding it back - http://discordpy.readthedocs.io/en/latest/api.html#message
# embed references - http://discordpy.readthedocs.io/en/latest/api.html#embed


"""
        async def on_message(self, message):
        author = message.author
        try:
            color = author.color
        except:
            color = 0x585858
        if self.toggle["toggle"] and author.id == self.bot.user.id:
            embed=discord.Embed(description=message.content, color=color)
            await self.bot.edit_message(message, new_content=" ", embed=embed)
"""

def setup(bot):
        action = embedthis(bot)
        bot.add_cog(action)