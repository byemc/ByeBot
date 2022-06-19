import os
from wsgiref import headers
from nextcord.ext import commands
import nextcord
import sys
import datetime, time #this is the important set for generating an uptime
import platform
import random
from dotenv import load_dotenv
import whois
import sqlite3
import requests,json
import server, aiohttp

myPermissionsInt = 405810835062

debugMode = False

version = (0,1,1)
verstring = f"{version[0]}.{version[1]}.{version[2]}"

#import .env variables
load_dotenv()

APIKEY = os.environ['DISCORD_API']

defaultHelp = commands.DefaultHelpCommand()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('|', '?', 'bye!', 'bb?', 'bb!', 'bye?'), help_command=defaultHelp)

@bot.event
async def on_ready():
    print(f"Connected to Discord as {bot.user.name} ({bot.user.id})")
    bot.server = server.HTTPServer(
        bot=bot,
        host="0.0.0.0",
        port="8000",
    )
    await bot.server.start()

    if debugMode:
        await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Currently in debug mode. Expect me to go down!"))
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
        embed.add_field(name="Creator", value="[Bye](https://bye.url.lol/twitter)", inline=True)
        embed.add_field(name="Hosting", value="[Contabo](https://contabo.com) VPS S", inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency*1000)}ms")
        embed.add_field(name="Language", value=f"Python {platform.python_version()}")
        embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
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
class GitHub(commands.Cog, name="GitHub"):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="repo", breif="See repo info", description="Gets info about a repository on GitHub")
    async def _repo(self,ctx,repo:str):
        userAvatarUrl = ctx.message.author.avatar
        async with ctx.channel.typing():

            repo_info_request = requests.get(f"https://api.github.com/repos/{repo}")
            repo_info = repo_info_request.json()


            embed = nextcord.Embed(title=f"{repo_info['full_name']}", description=f"{repo_info['description']}", url=f"{repo_info['html_url']}")
            
            embed.set_thumbnail(url=f"{repo_info['owner']['avatar_url']}")

            embed.add_field(name="Owner", value=f"{repo_info['owner']['login']}")
            embed.add_field(name="Stars", value=f"{repo_info['stargazers_count']}", inline=True)
            embed.add_field(name="Forks", value=f"{repo_info['forks_count']}", inline=True)
            embed.add_field(name="Watchers", value=f"{repo_info['watchers_count']}", inline=True)
            embed.add_field(name="Open Issues", value=f"{repo_info['open_issues_count']}", inline=True)
            embed.add_field(name="Language", value=f"{repo_info['language']}", inline=True)
            embed.add_field(name="License", value=f"{repo_info['license']}", inline=True)
            embed.add_field(name="Is a fork?", value=f"{repo_info['fork']}")
            embed.add_field(name="Created at", value=f"{repo_info['created_at']}", inline=True)
            embed.add_field(name="Updated at", value=f"{repo_info['updated_at']}", inline=True)
            embed.add_field(name="Pushed at", value=f"{repo_info['pushed_at']}", inline=True)


            embed.set_author(name=f"ByeBot", icon_url=f"{bot.user.avatar}")
            embed.set_footer(text=f"Requested by {ctx.message.author} | Remaining GET requests: {repo_info_request.headers['X-RateLimit-Remaining']}", icon_url=userAvatarUrl)
        await ctx.send(embed=embed)

@server.add_route(path="/info", method="GET")
async def http_info(request):
    return aiohttp.web.json_response(data={"online": True, "version": verstring, "verarray": [version[0], version[1], version[2]], "debug": debugMode}, status=200, headers={"Access-Control-Allow-Origin": "www.byemc.xyz"})
@server.add_route(path="/", method="GET")
async def http_index(request):
    '''Returns a redirect to `byemc.xyz/byebot`'''
    return aiohttp.web.HTTPFound(location="https://byemc.xyz/byebot")

# Add Cogs
bot.add_cog(misc(bot))
bot.add_cog(fun(bot))
bot.add_cog(tools(bot))
#bot.add_cog(GitHub(bot))

bot.run(APIKEY)
