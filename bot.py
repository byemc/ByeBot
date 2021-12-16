import os
from nextcord.ext import commands
import nextcord
import sys
import datetime, time #this is the important set for generating an uptime
import platform
import random
from dotenv import load_dotenv
import whois

myPermissionsInt = 405810835062

#import .env variables
load_dotenv()

APIKEY = os.environ['DISCORD_API']

defaultHelp = commands.DefaultHelpCommand()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('|', '?', 'bye!', 'bb?', 'bb!', 'bye?'), help_command=defaultHelp)

@bot.event
async def on_ready():
    print(f"Connected to Discord as {bot.user.name} ({bot.user.id})")
    global startTime #global variable to be used later in cog
    startTime = time.time() #snapshot of time when listener sends on_ready

guild_ids = [827083552155238460, 885454145346232361] # Put your server ID in this array.

# Regular commands (command_prefix)

class misc(commands.Cog, name='Misc.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo", aliases=["info", "bot"], brief="Info about the bot", description="Info about the bot")
    async def _botinfo(self, ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        userAvatarUrl = ctx.message.author.avatar
        embed=nextcord.Embed(title="ByeBot Details", description=f"Running on {len(self.bot.guilds)} servers")
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_author(name=f"ByeBot", icon_url=f"{self.bot.user.avatar}")
        embed.add_field(name="Creator", value="[Bye](https://twitter.com/_byemc)", inline=True)
        embed.add_field(name="Server", value="Replit", inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency*1000)}ms")
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
        embed.add_field(name="Language", value=f"Python {platform.python_version()}")
        await ctx.send(embed=embed)

    @commands.command(name="avatar", brief="Get a user's avatar", description="Returns the avatar of the requested user")
    async def _avatar(self, ctx, member: nextcord.Member):
        userAvatarUrl = ctx.message.author.avatar
        embed=nextcord.Embed(title=f"{member.display_name}'s avatar")
        embed.set_author(name=f"ByeBot", icon_url=f"{bot.user.avatar}")
        embed.set_image(url=member.avatar)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
        await ctx.send(embed=embed)

    @commands.command(name="ping", brief="Times the latency of the bot", description="Finds the amount of time between sending the message and the bot responding. Returns an embed with the time in ms")
    async def _ping(self, ctx):
        userAvatarUrl = ctx.message.author.avatar
        embed=nextcord.Embed(title=":ping_pong: Pong!", description=f"{round(self.bot.latency*1000)}ms")
        embed.set_author(name="ByeBot", icon_url=bot.user.avatar)
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
        await ctx.send(embed=embed)


class fun(commands.Cog, name='Fun'):
    '''Things that are fun... *i hope!*'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dice", brief="Roll a die... or maybe two!", description="Picks a number between 1 and 6, or between 1 and the number provided multiplied by 6.")
    async def dice(self,ctx,no_of_dice=1):
        result = random.randint(1,(6*int(no_of_dice)))
        await ctx.send(f"{ctx.message.author.mention} You rolled a {result}!")

class tools(commands.Cog, name="Tools"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinvite", brief="Get the invite link for a bot", description="Makes an invite link for a requested bot. Made by Taureon#5684 (492665478687490048)")
    async def _botinvite(self,ctx,thebot:nextcord.Member,permissions:int=8):
        userAvatarUrl = ctx.message.author.avatar
        if permissions == 8:
            await ctx.send(":warning: WARNING: This link gives the bot admin perms! For more information about permissions integers, please see the attached link. https://discordapi.com/permissions.html")
        embed=nextcord.Embed(title=f"{thebot.display_name}'s invite link", description=f"[Here you go!](https://discord.com/oauth2/authorize?client_id={thebot.id}&scope=bot&permissions={permissions})")
        embed.set_author(name=f"ByeBot | Thanks to Taureon!", icon_url=f"{bot.user.avatar}")
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
        await ctx.send(embed=embed)

    @commands.command(name="whois", brief="Run a WHOIS search on an IP or web address.", description="Runs a WHOIS search on an IP or web address.")
    async def _whois(self,ctx,query,value=None):
        '''
        Run a WHOIS search on an IP or web address. 
        INPUTS:
        query: The IP/Site you want to search for.
        value: The value you want. You can leave this blank for an overview. Please use a key returned by "python-whois", like "org"'''

        async with ctx.channel.typing():
            if value == None:
                userAvatarUrl = ctx.message.author.avatar
                embed=nextcord.Embed(title=f"WHOIS Lookup for {query}")
                query = whois.whois(query)
                embed.set_author(name=f"ByeBot", icon_url=f"{bot.user.avatar}")
                embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
                for result in query:
                    if (result == "updated_date" and query[result] == list):
                        embed.add_field(name="Updated Date", value=f"{query[result][0]}")
                    elif type(query[result]) == list:
                        embed.add_field(name=f"{result}", value=f"{query[result][1]}", inline=True)
                    else:
                        embed.add_field(name=f"{result}", value=f"{query[result]}", inline=True)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{ctx.message.author.mention} The {value} for {query} is `{whois.whois(query)[value]}`")

    @_whois.error
    async def whois_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.message.author.mention} Please provide a domain or IP. EG. `google.com` or `1.1.1.1`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.message.author.mention} BadArgument.")

# Add Cogs
bot.add_cog(misc(bot))
bot.add_cog(fun(bot))
bot.add_cog(tools(bot))

bot.run(APIKEY)
