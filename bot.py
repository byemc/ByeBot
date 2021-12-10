import os
from nextcord.ext import commandsimport nextcord
import sys
import datetime, time #this is the important set for generating an uptime
import platform
import random
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.environ['DISCORD_API']

defaultHelp = commands.DefaultHelpCommand()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('|', '?'), help_command=defaultHelp)

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
        embed.set_author(name="ByeBot", icon_url=f"{bot.user.avatar}")
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

# Add Cogs
bot.add_cog(misc(bot))
bot.add_cog(fun(bot))

bot.run(APIKEY)
