import discord
from discord.ext import commands
from rls.rocket import RocketLeague
import json
from .utils import checks
import urllib
import pprint

class memlostats:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that retrieves a user's Rocket League rank based on gamertag and platform input and sets a role"""

        def __init__(self, bot):
                self.bot = bot
                self.image = "data/rlstats/signature.png"
                self.json = "data/rlstats/rlstats.json"
                self.legend = "data/rlstas/tierlegend.json"

        @commands.command(pass_context=True)
        async def stats(self, ctx, platform, gamertag):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                data = ctx.message.content.strip()
                if "stats" in data:
                        returndata = self.getrank(platform, gamertag)
                        if "success" in returndata:
                                await self.discordsendfile(channel, self.image)
                                returnrank = str(self.parseforrank())
                                if "Fail" in returnrank:
                                        pass
                                else:
                                        await self.discordsay("Your highest rank is `" + returnrank + "`.")

        def getrank(self, platform, gamertag):
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
                        playerdata = rocket.players.player(id=gamertag, platform=platformid)
                        playerjson = str(playerdata.json())
                        with open(self.json, "w") as f:
#                                f.write(str(playerdata.json()))
                                json.dump(playerdata, f)
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(playerdata.json()['signatureUrl'], self.image)
                        result = "success"
                        return result

        def parseforrank(self):
                """sort through self.json and return highest rank"""
                latestseason = "7"
                with open(self.json, 'r') as f:
                        data = f.read()
                        playerdata = json.loads(data)
                        return playerdata
                        #playerdata[0] = json.loads(f)
#                return playerdata
#                playerdata = json.load(open(self.json))
#                        for k,v in playerdata['rankedSeasons'].items():
#                                if latestseason == k:
#                                        ranks = v
#                                        break
#                        try:
#                                ranks
#                        except NameError:
#                                error = "Fail.  NameError when looking at ranks."
#                                return error
#                        else:
#                                return ranks
#                                if "7" in playerdata['rankedSeasons'].items():
#                                rank1v1 = playerdata['rankedSeasons'][latestseason]['10']
#                                rank2v2 = rank['11']
#                                rank3ss = rank['12']
#                                rank3v3 = rank['13']
#                                ranks = [rank1v1,rank2v2,rank3ss, rank3v3]
#                                maxrank = str(max(ranks))
#                        else: 
#                                error = "I don't have any data from the latest season."
#                                return error
#                with open(self.legend, "r") as legend:
#                        for k,v in self.legend.items():
#                                if maxrank == k:
#                                        namedrank = v
#                                        break
#                        try:
#                                namedrank
#                        except NameError:
#                                error = "Fail. Welp, a NameError occurred when looking at ranks"
#                                return error
#                        else:
#                                return namedrank

        async def discordsay(self, data):
                await self.bot.say(data)

        async def discordsendfile(self, channel, file):
                await self.bot.send_file(channel, file)

def setup(bot):
        action = memlostats(bot)
        bot.add_cog(action)