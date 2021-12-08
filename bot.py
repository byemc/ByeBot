import os
from discord.ext import commands
import discord
import sys
import datetime, time #this is the important set for generating an uptime

APIKEY = os.environ['DISCORD_API']


bot = commands.Bot(command_prefix='|')
@bot.event
async def on_ready():
    print("Connected to Discord")
    global startTime #global variable to be used later in cog
    startTime = time.time()# snapshot of time when listener sends on_ready

@bot.command()
async def info(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    userAvatarUrl = ctx.message.author.avatar_url
    embed=discord.Embed(title="ByeBot Details", description=f"Running on {len(bot.guilds)} servers")
    embed.set_author(name=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
    embed.add_field(name="Programmer", value="ByeMC", inline=True)
    embed.add_field(name="Server", value="Replit", inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)
    embed.set_footer(text="Hi there.")
    await ctx.send(embed=embed)

bot.run(APIKEY)
