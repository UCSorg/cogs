import discord
from discord.ext import commands
from rls.rocket import RocketLeague
import json
from .utils import checks
import urllib


class memlorolemanager:
        """Custom cog by Memlo, Matt Miller, that removes a Rocket League rank role from a/every user and sets only role to Rank Not Determined"""

        def __init__(self, bot):
                self.bot = bot

        @commands.command()
        async def userrolelist(self, member : discord.Member):
                """Lists the user's roles"""

                server = member.server
                uservar = member.name

                await self.bot.say("Processing for `" + uservar + "`")

                roleslist = member.roles
                await self.bot.say("User is a member of:  Everyone")
                for role in roleslist[1:]:
                        await self.bot.say(role)

        @commands.command()
        async def removeuserfromrole(self, member : discord.Member, role : discord.Role):
                """Removes a user from a role"""

                server = member.server
                uservar = member.name
                roleslist = member.roles

                if role in roleslist:
                        try:
                                await self.bot.remove_roles(member, role)
                                await self.bot.say("Role successfully removed.")
                        except discord.Forbidden:
                                await self.bot.say("I don't have permissions to manage roles!")
                        except discord.HTTPException:
                                await self.bot.say("I ran into an HTTP Exception error!")

                else:
                        await self.bot.say("User does not have that role.")

#       @commands.command(pass_context=True)
#       async def removeallusersfromrole(self, ctx,  role : discord.Role):
#               #Removes all user from a role
#
#               server = ctx.message.server
#               member = ctx.message.server
#
#               for member in server.members:
#                       if role in server.roles:
#                               try:
#                                       await self.bot.remove_roles(member, role)
#                                       await self.bot.say("Role successfully removed for `" + str(member) + "`.")
#                               except discord.Forbidden:
#                                       await self.bot.say("I don't have permissions to manage roles!")
#                               except discord.HTTPException:
#                                       await self.bot.say("I ran into an HTTP Exception error!")
#
#                       else:
#                               await self.bot.say("Role doesn't exist on server.")


def setup(bot):
        action = memlorolemanager(bot)
        bot.add_cog(action)
