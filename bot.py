import os
from discord.ext import commands
import discord
import sys
import datetime, time #this is the important set for generating an uptime
import platform
import logging

logging.basicConfig(level=logging.WARNING)

APIKEY = os.environ['DISCORD_API']

bot = commands.Bot(command_prefix=commands.when_mentioned_or('|'))

@bot.event
async def on_ready():
    print(f"Connected to Discord as {bot.user.name} ({bot.user.id})")
    global startTime #global variable to be used later in cog
    startTime = time.time()# snapshot of time when listener sends on_ready

guild_ids = [827083552155238460, 885454145346232361] # Put your server ID in this array.

# Regular commands (command_prefix)

@bot.command(name="info", description="Info about the bot")
async def _info(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    userAvatarUrl = ctx.message.author.avatar_url
    embed=discord.Embed(title="ByeBot Details", description=f"Running on {len(bot.guilds)} servers")
    embed.set_author(name=f"ByeBot", icon_url=f"{bot.user.avatar_url}")
    embed.add_field(name="Creator", value="ByeMC", inline=True)
    embed.add_field(name="Server", value="Replit", inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)
    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
    embed.add_field(name="Language", value=f"Python {platform.python_version()}")
    await ctx.send(embed=embed)

@bot.command(name="avatar", description="Returns the avatar of the requested user")
async def _avatar(ctx, member: discord.Member):
    userAvatarUrl = ctx.message.author.avatar_url
    embed=discord.Embed(title=f"{member.display_name}'s avatar")
    embed.set_author(name=f"ByeBot", icon_url=f"{bot.user.avatar_url}")
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=userAvatarUrl)
    await ctx.send(embed=embed)

bot.run(APIKEY)
