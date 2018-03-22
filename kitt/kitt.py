import discord
from discord.ext import commands
import requests
import os
from .utils import checks
from .utils.dataIO import dataIO
from cogs.rlrank import rlsapi
from __main__ import send_cmd_help
import urllib.request

"""Requirement!  must have rlrank cog installed"""


#"Gotta be quicker than that."
#"Ooo, so close."
#"I hit an exception wall, it's probably me, not you.  You're perfect.  Definitely not you."

hubdatapath = "data/rlrank/hubdata.json"
hubtdatadefault = {}
apipath = "data/rlrank/rls-apikey.json"
tierlegend =    {1:"Bronze I", 2:"Bronze II",3:"Bronze III",4:"Silver I",5:"Silver II",6:"Silver III",
                7:"Gold I",8:"Gold II",9:"Gold III",10:"Platinum I",11:"Platinum II",12:"Platinum III",
                13:"Diamond I",14:"Diamond II",15:"Diamond III",16:"Champion I",17:"Champion II",18:"Champion III",19:"Grand Champion"}
tempauthorpath = "data/rlrank/authordata.json"
bothelp = "**General Utilities**\n  <@420082619611611137> - `-help`\n  @Dyno#3861 - <https://www.dynobot.net/commands>\n**Stats Tracking**\n  @Stat Tracker - <http://bots.tracker.network/commands.html>\n  @RLTracker.pro - <https://rltracker.pro/discord>\n  @RLTrader - <https://rltracker.pro/discord>\n**Music**\n  @Torque#6847 - `-help Audio`\n  @Mee6#4876 - <https://mee6.xyz/about>\n  @Dyno#3861 - <https://www.dynobot.net/commands>\n**Streaming**\n  @Now Live - <http://nowlivebot.com/commands>"

class kitt:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that interacts with authors and does a few different things."""

        def __init__(self, bot):
                self.bot = bot
                self.apikey = dataIO.load_json(apipath)

        @commands.command(pass_context=True)
        async def kitt(self, ctx):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = ctx.message.author
                user = str(author).split('#',1)[0]
                nlpBase = ["basicinfo", "basic", "info"]
                nlpRLRank = ["rlrank", "rank", "rocket", "league"]
                nlpAboutMe = ["aboutme", "about"]
                nlpRegion = ["region", "location", "live", "area", "home"]
                nlpHelp = ["how do i?", "how do i", "help", "halp"]
                todo = await self.question(ctx,"Hey %s!  What can I help you do today? Some keywords are: %s, %s, %s, %s, %s " % (user, nlpBase[0], nlpRLRank[0], nlpAboutMe[0], nlpRegion[0], nlpHelp[0]))
                if todo == None:
                        pass
                elif todo.lower() in nlpBase:
                        await self.kittbasicinfo(ctx)
                elif todo.lower() in nlpRLRank:
                        await self.kittrlrank(ctx)
                elif todo.lower() in nlpAboutMe:
                        await self.kittaboutme(ctx)
                elif todo.lower() in nlpRegion:
                        await self.kittregion(ctx)
                elif todo.lower() in nlpHelp:
                        await self.discordsay(bothelp)
                else:
                        await self.discordsay("I'm not set up to do really anything else at this time.")   

        async def kittbasicinfo(self, ctx):
                """Find gamerid and platform for author"""
                author = str(ctx.message.author)
                user = author.split('#',1)[0]
                channel = ctx.message.channel
                acceptedplatforms = ['pc', 'ps4', 'xbox']
                gamerid = await self.question(ctx,"Hey `" + user + "`!  Can I get your gamertag ID?")
                platform = await self.question(ctx, "What platform is that for?")
                if platform.lower() in "switch":
                        content = Embed(title="Error", description="The Nintendo Switch is not supported for stat tracking.", color=16713736)
                        await self.discordembed(channel, content)
                elif platform.lower() not in acceptedplatforms:
                        content = Embed(title="Error", description="I don't think `%s` is accepted.  Have you tried turning it off and on again?" % (platform), color=16713736)
                        await self.discordembed(channel, content)
                else:
                        confirmation = await self.question(ctx, "Do you want me to store this for future use?")
                        if "yes" in confirmation.lower():
                                tmp = dataIO.load_json(hubdatapath) #store anything we've gathered so far
                                tmp[author] = {}
                                tmp[author]["baseInfo"] = {"platform": platform, "gamerid": gamerid}
                                dataIO.save_json(hubdatapath, tmp)

        async def kittrlrank(self, ctx):
                """Find rocket league stats for author"""
                author = ctx.message.author
                channel = ctx.message.channel
                data = dataIO.load_json(hubdatapath)
                apikey = self.apikey.get("key")
                try:
                        baseinfodict = data[author]["baseInfo"]
                        gamerid = baseinfodict["gamerid"]
                        platform = baseinfodict["platform"]
                except NameError:
                        await self.discordsay("I'm going to need some more information first.")
                        await self.kittbasicinfo(ctx)
                        await self.kittrlrank(ctx)
                except KeyError:
                        await self.discordsay("I'm going to need some more information first.")
                        await self.kittbasicinfo(ctx)
                        await self.kittrlrank(ctx)
                else:
                        platformlegend = {'pc' : 1, 'ps4' : 2, 'xbox' : 3}
                        for k,v in platformlegend.items(): #using the platform legend, find the platform ID
                            if platform == k:
                                platformid = v
                                break
                        try:
                            platformid
                        except NameError:
                            await self.discordsay("Fail. rlsapi NameError for platform - ask an admin")
                        else:
                            try:
                                headers = {'Authorization' : apikey}
                                params = (('unique_id', gamerid), ('platform_id', platformid),)
                                data = requests.get('https://api.rocketleaguestats.com/v1/player', headers=headers, params=params)
                                playerdata = data.json()
                            except NameError:
                                await self.discordsay("Fail. rlsapi NameError for API CURL Request - ask an admin")
                            else:
                                if "code" in playerdata:
                                    error = "Fail. Error: %s. %s  gamertag=%s, platform=%s" % (str(playerdata['code']),playerdata['message'],gamertag,platformid)
                                    await self.discordsay(error)
                                elif "Fail" in playerdata: #if error code, respond with error code message
                                        content = Embed(title="Error", description=data, color=16713736)
                                        await self.discordembed(channel, content)
                                else:
                                        playerurl = playerdata.get("profileUrl")
                                        playersignature = playerdata.get("signatureUrl")
                                        try:
                                            playerurl
                                            playersignature
                                        except NameError:
                                            content = Embed(title="Error", description="I had trouble finding information about you on rocketleaguestats.com", color=16713736)
                                            await self.discordembed(channel, content)
                                        else:
                                                await self.discordsay("This is what we have: " + playersignature)
                                                confirmation = await self.question(ctx, "Is this you?")
                                                if "yes" in confirmation.lower():
                                                        tmp = dataIO.load_json(hubdatapath) #store the data about the player for use later
                                                        tmp[author]['rldata'] = playerdata
                                                        dataIO.save_json(hubdatapath, tmp)
                                                        confirmation = await self.question(ctx, "Do you want to set your rank for this server with this information?")
                                                        if "yes" in confirmation.lower():
                                                                await self.discordsay("Process for setting rank goes here.")
                                                        elif "no" in confirmation.lower():
                                                                await self.discordsay("Okay, no changes have been made.")
                                                else:
                                                        await self.discordsay("I think we'll need to start over.")

        async def kittaboutme(self, ctx):
                """Return stored information about the author"""
                author = str(ctx.message.author)
                channel = ctx.message.channel
                try:
                        authordict = dataIO.load_json(hubdatapath)[author]
                except KeyError:
                        await self.discordsay("I don't have anything about you saved.  Let's fix that.")
                        await self.kittbasicinfo(ctx)
                else:
                        dataIO.save_json(tempauthorpath, authordict)
                        await self.discordsendfile(channel, tempauthorpath) 

        async def kittregion(self, ctx):
                """Set the Region Role"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = ctx.message.author
                nlpregionEU = ["eu", "europe"]
                nlpregionNA = ["na", "us"]
#                nlpregionNAEast = ["east", "us-east", "na-east"]
#                nlpregionNAWest = ["west", "us-west", "na-west"]
                region = await self.question(ctx,"What region do you game in?  Multiple answers are accepted: %s, %s" % (nlpregionNA[0], nlpregionEU[0]))
                regionsplit = region.split()
                for answer in regionsplit:
                        if answer.lower() in nlpregionEU:
                                await self.discordassignrole(server, author, "EU")
                        elif answer.lower() in nlpregionNA:
                                await self.discordassignrole(server, author, "NA")
#                        elif answer.lower() in nlpregionNAEast:
#                                await self.discordsay("You are now in the region: US-East.")
#                        elif answer.lower() in nlpregionNAWest:
#                                await self.discordsay("You are now in the region: US-West.")
                        else:
                                await self.discordsay("I have made no changes because %s is not in my accepted regions." % (answer))

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

        #common discord functions start
        async def discordsay(self, data):
                """send message in discord"""
                await self.bot.say(data)
        async def discordsendfile(self, channel, file):
                """Send attachment in discord"""
                await self.bot.send_file(channel, file)
        async def discordembed(self, channel, content):
                """Send embed message in discord"""
                await self.bot.send_message(channel, embed=content)
        async def discordwaitformessage(self, ctx):
                """Wait for message and return answer back to function"""
                message = await self.bot.wait_for_message(timeout=90,author=ctx.message.author, channel=ctx.message.channel)
                return message
        async def question(self, ctx, question):
                """Send question in message and return answer back to function"""
                await self.bot.say(question)
                response = await self.discordwaitformessage(ctx)
                if response is not None:
                        return response.content
                else:
                        await self.discordsay("I can't wait forever, %s.  maybe we can try again later." % (ctx.message.author))  
                        return None
        async def discordassignrole(self, server, member, newrole):
                """Assign a role to a user"""
                for role in server.roles:
                        if role.name == newrole:
                                addrole = role
                                break
                try:
                        addrole
                except discord.errors.Forbidden:
                        await self.discordsay("Try checking bot permissions!")
                except:
                        await self.discordsay("Try checking the role again!")
                else:
                        if addrole not in member.roles:
                                await self.bot.add_roles(member, addrole)
                                await self.discordsay("You are now a member of %s" % (addrole.name))
                        else:
                                await self.discordsay("You are already a member of %s" % (addrole.name))
        #common discord functions end

def check_folders():
    if not os.path.exists("data/rlrank"):
        print("Creating data/rlrank folder...")
        os.makedirs("data/rlrank")

def check_files():
    f = hubdatapath
    if not dataIO.is_valid_json(f):
        print("Creating hubdata.json...")
        dataIO.save_json(f, hubtdatadefault)

def setup(bot):
        check_folders()
        check_files()
        action = kitt(bot)
        bot.add_cog(action)
