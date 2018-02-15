import discord
from discord.ext import commands
from rls.rocket import RocketLeague
import json
from .utils import checks
import urllib

class RLstats:
        """Custom cog by Eny, Patrik Srna, that retrieves an embed image of user's Rocket League rank based on SteamID input"""

        def __init__(self, bot):
                self.bot = bot
                self.image = "data/rlstats/signature.png"

        @commands.command()
        async def rlstats(self, steamidinput):
                """Retrieves Rocekt League Statistics from rocketleaguestats.com using their API"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                steamid = str(steamidinput)
                response = rocket.players.player(id=steamid, platform=1)
                signatureUrl = response.json()['signatureUrl']
                await self.bot.say(signatureUrl)

        @commands.command(pass_context=True, no_pm=True)
        @checks.mod_or_permissions(manage_roles=True)
        async def rlstats2(self, ctx, steamidinput):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                steamid = str(steamidinput)
                response = rocket.players.player(id=steamid, platform=1)
                signatureUrl = response.json()['signatureUrl']
                server = ctx.message.server
                channel = ctx.message.channel
                try:
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom$
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(signatureUrl, self.image)
                        await self.bot.send_file(channel, self.image)
                except urllib.error.HTTPError:
                        await self.bot.say("Welp, looks like I ran into an HTTP Error")



def setup(bot):
        bot.add_cog(RLstats(bot))

