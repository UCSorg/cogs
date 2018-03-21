import discord
from discord.ext import commands
import requests
import os
from .utils import checks
from .utils.dataIO import dataIO
from cogs.rlrank import rlrank
from __main__ import send_cmd_help
import urllib

"""Requirement!  must have rlrank cog installed"""


#"Gotta be quicker than that."
#"Ooo, so close."
#"I hit an exception wall, it's probably me, not you.  You're perfect.  Definitely not you."

hubdatapath = "data/rlrank/hubdata.json"
hubtdatadefault = {}
tierlegend =    {1:"Bronze I", 2:"Bronze II",3:"Bronze III",4:"Silver I",5:"Silver II",6:"Silver III",
                7:"Gold I",8:"Gold II",9:"Gold III",10:"Platinum I",11:"Platinum II",12:"Platinum III",
                13:"Diamond I",14:"Diamond II",15:"Diamond III",16:"Champion I",17:"Champion II",18:"Champion III",19:"Grand Champion"}
tempauthorpath = "data/rlrank/authordata.json"

class kitt:
        """Custom cog by Memlo and Eny, Matt Miller and Patrik Srna, that interacts with authors and does a few different things."""

        def __init__(self, bot):
                self.bot = bot

        @commands.command(pass_context=True)
        async def kitt(self, ctx):
                """Let's chat"""
                server = ctx.message.server
                channel = ctx.message.channel
                author = str(ctx.message.author)
                if ctx.invoked_subcommand is None:
                        todo = await self.question(ctx, "Hey %s!  What would you like to do today? Keywords are: baseinfo, rlrank, region, stats, aboutme" % (author))
                        await self.discordsay(todo)
                        if "base" or "baseinfo" or "info" in todo.lower():
                                await self.kittbaseinfo(ctx)
                        elif "rlrank" or "rocket" or "league" or "rank" in todo.lower():
                                await self.kittrlrank(ctx)
                        elif "about" or "aboutme" in todo.lower():
                                await self.kittaboutme(ctx)
                        else:
                                await self.discordsay("I'm not set up to do really anything else at this time.")   

        async def kittbaseinfo(self, ctx):
                """Find gamerid and platform for author"""
                author = str(ctx.message.author)
                channel = ctx.message.channel
                acceptedplatforms = ['pc', 'ps4', 'xbox']
                await self.bot.say("Hey `" + author + "`!  Can I get your gamertag ID?")
                gameridresponse = await self.bot.wait_for_message(author=ctx.message.author)
                gamerid = gameridresponse.content.lower().strip()
                if gameridresponse == "none":
                        content = Embed(title="Error", description="No gamertag ID response.", color=16713736)
                        await self.discordembed(channel, content)
                        pass
                else:
                        await self.bot.say("What platform is that for? note: Switch not supported currently")
                        platformresponse = await self.bot.wait_for_message(author=ctx.message.author)
                        platform = platformresponse.content.lower().strip()
                        if platformresponse == "none":
                                content = Embed(title="Error", description="No platform response.", color=16713736)
                                await self.discordembed(channel, content)
                                pass
                        elif platform.lower() in "switch":
                                content = Embed(title="Error", description="The Nintendo Switch is not supported for stat tracking.", color=16713736)
                                await self.discordembed(channel, content)
                                pass
                        elif platform.lower() not in acceptedplatforms:
                                content = Embed(title="Error", description="I don't think `%s` is accepted.  Have you tried turning it off and on again?" % (platform), color=16713736)
                                await self.discordembed(channel, content)
                                pass
                        else:
                                confirmation = await self.question(ctx, "Do you want me to store this for future use?")
                                if "yes" in confirmation.lower():
                                        tmp = dataIO.load_json(hubdatapath) #store anything we've gathered so far
                                        tmp[author] = {}
                                        tmp[author]["baseInfo"] = {"platform": platform, "gamerid": gamerid}
                                        dataIO.save_json(hubdatapath, tmp)

        async def kittrlrank(self, ctx):
                """Find rocket league stats for author"""
                author = str(ctx.message.author)
                data = dataIO.load_json(hubdatapath)
                try:
                        baseinfodict = data[author]["baseInfo"]
                        gamerid = baseinfodict["gamerid"]
                        platform = baseinfodict["platform"]
                except NameError:
                        await self.bot.say("I'm going to need some more information first.")
                        await self.baseinfo(ctx)
                else:
                        playerdata = rlrank.rlrank(ctx, platform, gamerid)
                        confirmation = await self.question(ctx, "Is this you?")
                        if "yes" in confirmation.lower():
                                tmp = dataIO.load_json(hubdatapath) #store the data about the player for use later
                                tmp[author]['rldata'] = playerdata
                                dataIO.save_json(hubdatapath, tmp)
                                confirmation = await self.question(ctx, "Do you want to set your rank for this server with this information?")
                                if "yes" in confirmation.lower():
                                        await self.bot.say("Process for setting rank goes here.")
                                elif "no" in confirmation.lower():
                                        await self.bot.say("Okay, no changes have been made.")
                        else:
                                await self.bot.say("I think we'll need to start over.") 

        async def kittaboutme(self, ctx):
                """Return stored information about the author"""
                author = str(ctx.message.author)
                try:
                        authordict = dataIO.load_json(hubdatapath)[author]
                except NameError:
                        await self.discordsay("I don't have anything about you saved.")
                else:
                        dataIO.save_json(tempauthorpath, authordict)
                        await self.discordsendfile(channel, tempauthorpath) 

        async def question(self, ctx, question):
                await self.bot.say(question)
                response = await self.bot.wait_for_message(author=ctx.message.author)
                return response.content

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
                """Simple text in discord"""
                await self.bot.say(data)

        async def discordsendfile(self, channel, file):
                """Simple attachment in discord"""
                await self.bot.send_file(channel, file)

        async def discordembed(self, channel, content):
                """Simple embed in discord"""
                await self.bot.send_message(channel, embed=content)

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
