import discord
from discord.ext import commands
from rls.rocket import RocketLeague
import json
from .utils import checks
import urllib

class memlorlrankupdate:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that retrieves a user's Rocket League rank based on SteamID input and sets a role"""

        def __init__(self, bot):
                self.bot = bot
                self.image = "data/rlstats/signature.png"
                self.json = "data/rlstats/rlstats.json"
                self.legend = "data/rlstas/tierlegend.json"

        @commands.command(pass_context=True)
        async def gadget(self, ctx):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                data = ctx.message.content.strip()
                if "gadget" in data:
                        steamiddict = await self.steamid(ctx)
                        if "success" in steamiddict['1']:
                                rankdict = self.getrank(steamiddict['2'], steamiddict['3'])
                                if "success" in rankdict['result']:
                                        await self.bot.send_file(channel, self.image)
                                else:
                                        await self.bot.say(returndata)
                        else:
                                pass

#               try:
#                       returndata = self.getrank(channel, author, response, response2)
#                                               if "success" in returndata['result']:
#                                                       await self.bot.send_file(channel, self.image)
#                                                       await self.bot.say("Hey `" + author + "` is this you?")
#                                               else:
#                                                       await self.bot.say(returndata)
#                                       except AttributeError:
#                                               await self.bot.say("Looks like I ran into an exception")
#                               except TypeError:
#                                       await self.bot.say("I hit an exception wall, it's probably me, not you.  You're perfect.  Definitely not you.")
#                       response3dirty = await self.bot.wait_for_message(author=ctx.message.author)
#                       response3 = response3dirty.content.lower().strip()
#                       if response3dirty == "none":
#                               pass
#                       elif "yes" in response:
#                               rank = parseforrank()
#                               await self.bot.say("Here's where I would set your rank to " + rank)
#                       elif "no" in response:
#                               await self.bot.say("We might need to start over.")
#                       else:
#                               await self.bot.say("Your answer wasn't  worth my time.")

        async def steamid(self, ctx):
                author = str(ctx.message.author)
                await self.bot.say("Hey `" + author + "`!  Can I get your steamID?")
                steamidresponse = await self.bot.wait_for_message(author=ctx.message.author)
                if steamidresponse == "none":
                        pass
                else:
                        await self.bot.say("Are you on **PC**, **PS4**, or **XBOX**?  note: Switch not supported currently")
                        platformresponse = await self.bot.wait_for_message(author=ctx.message.author)
                        if platformresponse == "none":
                                pass
                        else:
                                steamid = steamidresponse.content.lower().strip()
                                platform = platformresponse.content.lower().strip()
                                dict = { '1': 'success', '2' : steamid, '3' : platform}
                                await self.bot.say("I will try `" + steamid + "` on `" + platform + "`." )
                                return dict

        def getrank(self, steamidinput, platforminput):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                steamid = str(steamidinput)
                platform = str(platforminput)
                if "pc" in platform.lower():
                        response = rocket.players.player(id=steamidinput, platform=1)
                        self.json = response.json()
                elif "ps4" in platform.lower():
                        response = rocket.players.player(id=steamidinput, platform=2)
                        signatureUrl = response.json()['signatureUrl']
                elif "xbox" in platform.lower():
                        response = rocket.players.player(id=steamidinput, platform=3)
                        signatureUrl = response.json()['signatureUrl']
                try:
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(self.json['signatureUrl'], self.image)
                        result = "success"
                        return result
                except urllib.error.HTTPError:
                        error = "Welp, looks like I ran into an HTTP Error"
                        return error

        async def discordsay(self, data):
                await self.bot.say(data)

        async def discordsendfile1(self, channel):
                channel = channel
                author = author
                file = file
                await self.bot.send_file(channel, self.image)
                await self.bot.say("Hey `" + author + "` is this you?")

        def parseforrank():
                """sort through self.json and return highest rank"""
                latestseason = "7"
                rank = self.json['rankedSeasons'][latestseason]
                rank1v1 = rank['10']
                rank2v2 = rank['11']
                rank3ss = rank['12']
                rank3v3 = rank['13']
                ranks = [rank1v1,rank2v2,rank3ss, rank3v3]
                maxrank = str(max(ranks))
                return maxrank
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

def setup(bot):
        action = memlorlrankupdate(bot)
        bot.add_cog(action)