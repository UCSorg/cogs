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

        @commands.command(pass_context=True)
        async def gadget(self, ctx):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                data = ctx.message.content.strip()
                if "gadget" in data:
                        await self.bot.say("Hey `" + author + "`!  Can I get your steamID?")
                        responsedirty = await self.bot.wait_for_message(author=ctx.message.author)
                        response = responsedirty.content.lower().strip()
                        if responsedirty == "none":
                                pass
                        else:

                                try:
                                        await self.bot.say("I will try `" + response + "`")
#                                       await self.bot.say("Hang on,I'm going to try something.  Hold my hand, I'm scared")
                                        data = self.getrank(channel, author, response)
                                        if "success" in data:
                                                await self.bot.send_file(channel, self.image)
                                                await self.bot.say("Hey `" + author + "` is this you?")
                                        else: await self.bot.say(data)
                                except AttributeError:
                                        await self.bot.say("Looks like I ran into an exception")
#                               except TypeError:
#                                       await self.bot.say("I hit an exception wall, it's probably me, not you.  You're perfect.  Definitely not you.")
                        responsedirty = await self.bot.wait_for_message(author=ctx.message.author)
                        response = responsedirty.content.lower().strip()
                        if responsedirty == "none":
                                pass
                        elif "yes" in response:
                                await self.bot.say("Here's where I would set your rank.")
                        elif "no" in response:
                                await self.bot.say("We might need to start over.")
                        else:
                                await self.bot.say("Your answer wasn't  worth my time.")

        def getrank(self, channel, author, steamidinput):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                rocket = RocketLeague(api_key='ZEP7NZ0WLD9AFJ8WU15JZU5XD1XKM3TO')
                steamid = str(steamidinput)
                response = rocket.players.player(id=steamidinput, platform=1)
                signatureUrl = response.json()['signatureUrl']

                try:
                        opener=urllib.request.build_opener()
                        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        urllib.request.urlretrieve(signatureUrl, self.image)
                        success = "success"
                        return success
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


def setup(bot):
        action = memlorlrankupdate(bot)
        bot.add_cog(action)
