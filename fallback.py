import discord
import os
from discord.ext import commands
import sys
import configparser
import subprocess

if sys.argv[1] != "restart":
  prefix=sys.argv[1]
else:
  prefix="$"

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
  print('FALLBACK READY.')
  print(sys.argv)
  if sys.argv[1] == "restart":
    subprocess.Popen(['python3', 'ctx.py'])
    print('blah')
    channel = bot.get_channel(int(sys.argv[2]))
    await channel.send(embed=discord.Embed(title='Bot started.', color=0xFF0000))
    sys.exit(0)

@bot.command()
async def start(ctx):
  if ctx.author.id == 273845229130481665:
    message = await ctx.send(embed=discord.Embed(title='Starting bot...', description='', color=0xFFFFFF))
    subprocess.Popen(['python3', 'ctx.py'])
    await message.edit(embed=discord.Embed(title='Bot started.', description='', color=0xFF0000))
    sys.exit(0)

#this command is deprecated, use /update instead
@bot.command()
async def update(ctx):
  if ctx.author.id == 273845229130481665:
    await ctx.send(embed=discord.Embed(title='Updating bot...', description='', color=0xFF0000))
    os.system('git pull')

@bot.command()
async def ping(ctx):
  print('fallback pinged')
  await ctx.send('pong!')

config = configparser.ConfigParser()
config.read('cred.ini')
bot.run(config['config']['fessortoken'])
