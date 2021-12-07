from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='|')
@bot.event
async def on_ready():
    print("Connected to Discord")

@bot.command()
async def ban(ctx, user):
    await ctx.guild.ban(user)
    await ctx.send('Banned {}'.format(user))

@bot.command()
async def kick(ctx, user):
    await ctx.guild.kick(user)
    await ctx.send('Kicked {}'.format(user))

TOKEN = open('api.txt', 'r')
bot.run(TOKEN.read())
