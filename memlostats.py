import discord
from discord.ext import commands
from rls.rocket import RocketLeague
import json
import ast
from .utils import checks
import urllib
import pprint

class memlostats:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that retrieves a user's Rocket League rank based on gamertag and platform input and sets a role"""

        def __init__(self, bot):
                self.bot = bot
                self.image = "data/rlstats/signature.png"
                self.json = "data/rlstats/rlstats.json"
                self.legend = "data/rlstats/tierlegend.json"

        @commands.command(pass_context=True)
        async def stats(self, ctx, platform, gamertag):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                data = ctx.message.content.strip()
                latestseason = "7"
                if "stats" in data:
                        if "pc" or "ps4" or "xbox" in platform.lower():
                                returndata = self.getrank(platform.lower(), gamertag)
                                for k,v in returndata.items():
                                        if latestseason == k:
                                                allranks = v
                                                rank1v1 = allranks['10']['tier']
                                                rank2v2 = allranks['11']['tier']
                                                rank3ss = allranks['12']['tier']
                                                rank3v3 = allranks['13']['tier']
                                                break
                                ranks = [rank1v1,rank2v2,rank3ss,rank3v3]
                                maxrankint = str(max(ranks))
                                maxrank = self.matchtier(maxrankint)
                                await self.discordsendfile(channel, self.image)
                                await self.discordsay("Your highest rank is `" + maxrank + "`.")
                        else:
                                await self.discordsay("I'm pretty sure `" + platform + "` is not real.")

        def getrank(self, platform, gamertag):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                platformlegend = {'pc' : 1, 'ps4' : 2, 'xbox' : 3}
                for k,v in platformlegend.items(): #using the platform legend, find the platform ID
                        if platform == k:
                                platformid = v
                                break
                try:
                        platformid
                except NameError:
                        error = "Fail.  Welp a NameError occurred when looking at platform."
                        return error
                else:
                        try:
                                playerdata = rocket.players.player(id=gamertag, platform=platformid) #use the gamertag and platform ID to find the json formatted player data
#                                error = "Fail.  That's not a real player according to rocketleaguestats.com"
                        except HTTPError:
                                error = "There was an issue."
                        else:
                                rank = playerdata.json()['rankedSeasons']
                                with open(self.json, "w") as f: #save the json to a file for later (might not need to do this)
                                        json.dump(playerdata.json(), f)
                                opener=urllib.request.build_opener() #download and save the rocket league signature image
                                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                                urllib.request.install_opener(opener)
                                urllib.request.urlretrieve(playerdata.json()['signatureUrl'], self.image)
                                return rank

        def parsejson(self, file):
                """Take a json file and return dictionary"""
                with open(file, 'r') as f:
                        data = f.read()
                        data_dict = ast.literal_eval(data)
                        return data_dict

        def matchtier(self, rankint):
                """Using the RL Tier Legend, change the rankint into namedrank"""
                legend = self.parsejson(self.legend) #parse the legend json file
                for k,v in legend.items(): #loop through to find the rankint
                        if rankint == k:
                                namedrank = v
                                break
                try:
                        namedrank
                except NameError:
                        error = "Fail. Welp, a NameError occurred when looking at ranks"
                        return error
                else:
                        return namedrank

        async def discordsay(self, data):
                """Simple text in discord"""
                await self.bot.say(data)

        async def discordsendfile(self, channel, file):
                await self.bot.send_file(channel, file)

def setup(bot):
        action = memlostats(bot)
        bot.add_cog(action)