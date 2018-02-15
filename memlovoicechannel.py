import discord
from discord.ext import commands

class voicechannelsettings:
        """Custom cog by Memlo, Matt Miller, that messes with voice channels"""

        def __init__(self, bot):
                self.bot = bot

        @commands.command()
        async def userrolelist(self, member : discord.Member):
                """Keeps Channels on Flux"""
