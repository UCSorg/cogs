import discord
from discord.ext import commands
from discord import Embed
import requests
import os
from .utils import checks
from .utils.dataIO import dataIO
from __main__ import send_cmd_help
import urllib.request

apipath = "data/rlrank/rls-apikey.json"
apidefault = {"key" : "Error"}
tierlegend =    {1:"Bronze I", 2:"Bronze II",3:"Bronze III",4:"Silver I",5:"Silver II",6:"Silver III",
                7:"Gold I",8:"Gold II",9:"Gold III",10:"Platinum I",11:"Platinum II",12:"Platinum III",
                13:"Diamond I",14:"Diamond II",15:"Diamond III",16:"Champion I",17:"Champion II",18:"Champion III",19:"Grand Champion"}
hubdatapath = "data/rlrank/hubdata.json"
hubtdatadefault = {"discordid" : "playerData"}

class rlrank:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that retrieves a user's Rocket League stats based on gamertag and platform input"""

        def __init__(self, bot):
                self.bot = bot
                self.apikey = dataIO.load_json(apipath)

        @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
        @checks.admin_or_permissions(manage_server=True)
        async def rlrankapi(self, ctx):
                """Admin set RLS API Key.  This must be performed before using rlrank command."""
                if ctx.invoked_subcommand is None:
                        await send_cmd_help(ctx)

        @rlrankapi.command(pass_context=True, name="key")
        async def rlrankapi_key(self, ctx, *, apiresponse):
                """Set the RLS API Key"""
                channel = ctx.message.channel
                self.apikey['key'] = apiresponse
                dataIO.save_json(apipath, self.apikey)
                content = Embed(title="Success", description="I have successfully set your RLS API Key to: `" + apiresponse + "`", color=10604116)
                await self.discordembed(channel, content)

        @rlrankapi.command(pass_context=True, name="help")
        async def rlrankapi_help(self, ctx):
                """Specific instructions to get an RLS API Key."""
                channel = ctx.message.channel
                content = Embed(title="RLS API Key Information", description="Please click the link to get a RLS API Key", url="https://developers.rocketleaguestats.com/", color=16114700)
                await self.discordembed(channel, content)

        @commands.command(pass_context=True)
        async def rlrank(self, ctx, platform, *, gamertag : str):
                """Find your RL stats with a link"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                acceptedplatforms = ['pc', 'ps4', 'xbox']
                apikey = self.apikey['key']
                #reverse error handling for easier understanding
                if apikey == "Error":
                        content = Embed(title="Error", description="Please have an Admin set the API Key before using !rlrank.  Set the API Key using !rlrankapi.", color=16713736)
                        await self.discordembed(channel, content)
                else:
                        if platform.lower() in "switch":
                                content = Embed(title="Error", description="I'm sorry, but the Nintendo Switch is not supported for stat tracking.", color=16713736)
                                await self.discordembed(channel, content)
                        elif platform.lower() not in acceptedplatforms:
                                content = Embed(title="Error", description="I'm pretty sure platform, `" + platform + "`, is not a real console.", color=16713736)
                                await self.discordembed(channel, content)
                        else:
                                data = rlsapi(platform.lower(), gamertag, apikey) #send platform and gamertag to rlsapi function, get back either an error code or a dictionary
                                if "Fail" in data: #if error code, respond with error code message
                                        content = Embed(title="Error", description=data, color=16713736)
                                        await self.discordembed(channel, content)
                                else: #else find the player url and signature and respond with those
                                        playerurl = data.get("profileUrl")
                                        playersignature = data.get("signatureUrl")
                                        try:
                                                playerurl
                                                playersignature
                                        except NameError:
                                                content = Embed(title="Error", description="I had trouble finding information about you on rocketleaguestats.com", color=16713736)
                                                await self.discordembed(channel, content)
                                        else:
                                                image = "data/rlrank/playersignature.png"
                                                opener=urllib.request.build_opener() #download and save the rocket league signature image
                                                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                                                urllib.request.install_opener(opener)
                                                urllib.request.urlretrieve(playersignature, image)
                                                content = Embed(title="Click here for more detailed stats about %s" %(gamertag), description="This information updates about once per hour.", url=playerurl, color=10604116)
                                                await self.discordembed(channel, content)
                                                await self.discordsendfile(channel, image)
                                                tmp = dataIO.load_json(hubdatapath) #store the data about the player for use later
                                                tmp["discordid"] = author
                                                tmp[author] = data
                                                dataIO.save_json(hubdatapath, tmp)

        async def discordsay(self, data):
                """Simple text in discord"""
                await self.bot.say(data)

        async def discordsendfile(self, channel, file):
                """Simple attachment in discord"""
                await self.bot.send_file(channel, file)

        async def discordembed(self, channel, content):
                """Simple embed in discord"""
                await self.bot.send_message(channel, embed=content)

def rlsapi(platform, gamertag, apikey):
    """Retrieves Rocket League Stats image from rocketleaguestats.com using their API sends image back"""
    platformlegend = {'pc' : 1, 'ps4' : 2, 'xbox' : 3}
    for k,v in platformlegend.items(): #using the platform legend, find the platform ID
        if platform == k:
            platformid = v
            break
    try:
        platformid
    except NameError:
        return "Fail. rlsapi NameError - ask an admin"
    else:
        try:
            headers = {'Authorization' : apikey}
            params = (('unique_id', gamertag), ('platform_id', platformid),)
            playerdata = requests.get('https://api.rocketleaguestats.com/v1/player', headers=headers, params=params)
        except NameError:
            return "rlsapi NameError - ask an admin"
        else:
            if "displayName" in playerdata.json():
                dataIO.save_json("data/rlrank/player.json", playerdata.json())
                return playerdata.json()                
            elif "code" in playerdata.json():
                error = "Fail. Error: %s. %s  gamertag=%s, platform=%s" % (str(playerdata.json()['code']),playerdata.json()['message'],gamertag,platformid)
                return error
            else:
                return "Fail.  Not sure how we got here. - ask an admin"

def check_folders():
    if not os.path.exists("data/rlrank"):
        print("Creating data/rlrank folder...")
        os.makedirs("data/rlrank")

def check_files():
    f = apipath
    if not dataIO.is_valid_json(f):
        print("Creating rls-apikey.json...")
        dataIO.save_json(f, apidefault)
    g = hubdatapath
    if not dataIO.is_valid_json(g):
        print("Creating hubdata.json...")
        dataIO.save_json(g, hubtdatadefault)

def setup(bot):
        check_folders()
        check_files()
        action = rlrank(bot)
        bot.add_cog(action)