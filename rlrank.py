import discord
from discord.ext import commands
from discord import Embed
import rls
from rls.rocket import RocketLeague
import json
import ast
from .utils import checks
import urllib
import pprint

class rlrank:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that retrieves a user's Rocket League stats based on gamertag and platform input"""

        def __init__(self, bot):
                self.bot = bot
                self.image = "data/rlstats/signature.png"
                self.json = "data/rlstats/rlstats.json"
                self.legend = "data/rlstats/tierlegend.json"
                self.apikey = "data/rlstats/rls-api.json"

        @commands.command(pass_context=True)
        async def rlrank(self, ctx, platform, *, gamertag : str):
                """Find your RL stats with a link"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                acceptedplatforms = ['pc', 'ps4', 'xbox']
                #reverse error handling for easier understanding
                if platform.lower() not in acceptedplatforms:
                        await self.discordsay("I'm pretty sure `" + platform + "` is not a real console.")
                else:
                        returndata = self.getrank(platform.lower(), gamertag)
                        if "Fail" in returndata:
                                content = Embed(title="Error", description=returndata, color=16713736)
                                await self.discordembed(channel, content)
                        else:
                                playerurl = returndata["profileUrl"]
                                playersignature = returndata["signatureUrl"]
                                try:
                                        playerurl
                                        playersignature
                                except NameError:
                                        content = Embed(title="Error", description="I had trouble finding information about you on rocketleaguestats.com", color=16713736)
                                        await self.discordembed(channel, content)
                                else:
#                                        await self.discordsendfile(channel, self.image)
                                        await self.discordsay(playerurl)
                                        await self.discordsay(playersignature)
#                                        content = discord.Embed(title=gamertag, description="Here are your Rocket League ranks: [" + gamertag + "](" + playerurl + ")", url=playerurl, color=10604116, image=playersignature)
#                                        await self.discordembed(channel, content)

        def getrank(self, platform, gamertag):
                """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
                apikey = self.parsejson(self.apikey)[1] #call the API key from json file
                rocket = RocketLeague(api_key=apikey)
                platformlegend = {'pc' : 1, 'ps4' : 2, 'xbox' : 3}
                for k,v in platformlegend.items(): #using the platform legend, find the platform ID
                        if platform == k:
                                platformid = v
                                break
                try:
                        platformid
                except NameError:
                        return "getrank NameError - ask an admin"
                else:
                        try:
                                playerdata = rocket.players.player(id=gamertag, platform=platformid) #use the gamertag and platform ID to find the json formatted player data
                        except rls.exceptions.ResourceNotFound:
                                error = "Fail. There was an issue finding your gamertag in the <http://rocketleaguestats.com/> database."
                                return error
                        else:
                                rank = playerdata.json()['rankedSeasons']
                                with open(self.json, "w") as f: #save the json to a file for later (might not need to do this)
                                        json.dump(playerdata.json(), f)
                                opener=urllib.request.build_opener() #download and save the rocket league signature image
                                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                                urllib.request.install_opener(opener)
                                urllib.request.urlretrieve(playerdata.json()['signatureUrl'], self.image)
                                if "displayName" in playerdata.json():
                                        return rank
                                elif "code" in playerdata.json():
                                        error = "Fail. Error: " + playerdata.json()['code'] + ". " + playerdata.json()['message']
                                        return error
                                else:
                                        return "Fail.  Not sure how we got here."

        def parsejson(self, file):
                """Take a json file and return dictionary"""
                with open(file, 'r') as f:
                        data = f.read()
                        data_dict = ast.literal_eval(data)
                        return data_dict

        async def discordsay(self, data):
                """Simple text in discord"""
                await self.bot.say(data)

        async def discordsendfile(self, channel, file):
                """Simple attachment in discord"""
                await self.bot.send_file(channel, file)

        async def discordembed(self, channel, content):
                """Simple embed in discord"""
                await self.bot.send_message(channel, embed=content)

def setup(bot):
        action = rlrank(bot)
        bot.add_cog(action)