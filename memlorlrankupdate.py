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
                        try:
                                if steamiddict['1'] == "success":
                                        returndata = self.getrank(steamiddict['2'], steamiddict['3'])
                                        try:
                                                if "success" in returndata:
                                                        await self.bot.send_file(channel, self.image)
                                                        returnconfirmation = await self.confirmation(ctx)
                                                        try:
                                                                if "success" in returnconfirmation:
                                                                        await self.bot.say("I have something to do now that I'm not programmed for yet.")
                                                                else:
                                                                        await self.bot.say(returnconfirmation)  
                                                        except TypeError:
                                                                await self.bot.say("Gotta be quicker than that.")
                                                else:
                                                        await self.bot.say(returndata)
                                        except TypeError:
                                                await self.bot.say("Ooo, so close.")
                                else:
                                        pass
                        except TypeError:
                                await self.bot.say("I hit an exception wall, it's probably me, not you.  You're perfect.  Definitely not you.")

        async def steamid(self, ctx):
                user = str(ctx.message.author)
                await self.bot.say("Hey `" + user + "`!  Can I get your steamID?")
                steamidresponse = await self.bot.wait_for_message(author=ctx.message.author)
                if steamidresponse == "none":
                        pass
                else:
                        await self.bot.say("Are you on **PC**, **PS4**, or **XBOX**?  note: Switch not supported currently")
                        platformresponse = await self.bot.wait_for_message(author=ctx.message.author)
                        if platformresponse == "none":
                                pass
                        elif "pc" or "ps4" or "xbox" in platformresponse.content.lower():
                                steamid = steamidresponse.content.lower().strip()
                                platform = platformresponse.content.lower().strip()
                                dict = { '1': 'success', '2' : steamid, '3' : platform}
                                await self.bot.say("I will try `" + steamid + "` on `" + platform + "`." )
                                return dict
                        else:
                                await self.bot.say("I don't think `" + platformresponse.content + "` is accepted.  Have you tried turning it off and on again?")

        async def confirmation(self, ctx):
                await self.bot.say("Is this you?")
                confirmationresponse = await self.bot.wait_for_message(author=ctx.message.author)
                if confirmationresponse == "none":
                        pass
                elif "no" in confirmationresponse.content.lower():
                        await self.bot.say("I think we need to start over.")
#                       self.steamid(ctx)
                        result = "fail"
                        return result
                elif "yes" in confirmationresponse.content.lower():
                        result = "success"
                        return result
                else:
                        await self.bot.say("I don't have time for all these games.")

        def getrank(self, steamid, platform):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                platformlegend = {'pc' : 1, 'ps4' : 2, 'xbox' : 3}
                for k,v in platformlegend.items()
                        if platform == k,
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
                                f.write(playerdata.json())
                        pass
                try:
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(self.json['signatureUrl'], self.image)
                        result = "success"
                        return result

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
        action = memlorlrankupdate(bot)
        bot.add_cog(action)