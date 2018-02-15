import discord
from discord.ext import commands
from rls.rocket import RocketLeague
import json
from .utils import checks
import urllib

class memlostats:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that retrieves a user's Rocket League rank based on SteamID input and sets a role"""

        def __init__(self, bot):
                self.bot = bot
                self.image = "data/rlstats/signature.png"
                self.json = "data/rlstats/rlstats.json"
                self.legend = "data/rlstas/tierlegend.json"

        @commands.command(pass_context=True)
        async def stats(self, ctx, gamertag, platform):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                data = ctx.message.content.strip()
                if "stats" in data:
                        returndata = self.getrank(gamertag, platform)
                        await self.bot.say(returndata)

        def getrank(self, steamid, platform):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                platformlegend = {'pc' : 1, 'ps4' : 2, 'xbox' : 3}
                for k,v in platformlegend.items():
                        if platform == k:
                                platformid = v
                                break
                try:
                        platformid
                except NameError:
                        error = "Welp a NameError occurred when looking at platform."
                        return error
                else:
                        playerdata = rocket.players.player(id=steamid, platform=platformid)
                        with open(self.json, "w") as f:
                                f.write(str(playerdata.json()))
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(playerdata['signatureUrl'], self.image)
                        result = "success"
                        return result

        def parseforrank(self):
                """sort through self.json and return highest rank"""
                latestseason = "7"
                rank = self.json['rankedSeasons'][latestseason]
                rank1v1 = rank['10']
                rank2v2 = rank['11']
                rank3ss = rank['12']
                rank3v3 = rank['13']
                ranks = [rank1v1,rank2v2,rank3ss, rank3v3]
                maxrank = str(max(ranks))
                for k,v in self.legend.items():
                        if maxrank == k:
                                namedrank = v
                                break
                try:
                        namedrank
                except NameError:
                        error = "Welp, a NameError occurred when looking at ranks"
                        return error
                else:
                        return namedrank

        async def discordsay(self, data):
                await self.bot.say(data)

def setup(bot):
        action = memlostats(bot)
        bot.add_cog(action)