from base64 import decodebytes
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from discord.utils import get
import os
import discord
import discord.ext.commands
from discord.ext.commands import CommandNotFound
import asyncio
from functions.school import schedule
import datetime
import os,sys,inspect
from functions.fun.slander import slander
from configs import options
import configparser
from functions.school.lektiescanner import lektiescan
from threading import Timer
import pytz
import time
import platform
import git
from dateutil.relativedelta import relativedelta
import random
import string
import json
import functions.utils
startTime = time.time()
with open("data/data.json", "r") as file:
    data = json.load(file)
with open("data/data.json", "w") as file:
    data['startTime'] = startTime
    json.dump(data, file, indent=4)
def getUptime():
    uptime = time.time() - startTime
    return str(datetime.timedelta(seconds=uptime))

config = configparser.ConfigParser()
config.read('cred.ini')

if config['config']['mode'] == "updates":
  prefix = ','
else:
  prefix = '.'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_command(ctx):
  with open("data/log.txt", "a") as file:
    file.write(f"[{datetime.datetime.now()}] {ctx.author}: \"{ctx.message.content}\" | Message ID: {ctx.message.id} | Author ID: {ctx.author.id}\n")
  with open("data/data.json", "r") as file:
    data = json.load(file)
  try:
    data['useCount'] = data['useCount'] + 1
  except:
    data['useCount'] = 1
  data['lastUse'] = str(datetime.datetime.now())
  data['lastCommandUsed'] = ctx.message.content
  with open("data/data.json", "w") as file:
    json.dump(data, file)

@bot.event
async def on_ready():
  print('fessor is online.')
  await bot.change_presence(activity=discord.Game(name="matematikfessor.dk"))
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(embed=discord.Embed(title='Invalid kommando', description='Brug .help for en liste af kommandoer'))
        return
    elif isinstance(error, commands.CheckFailure):
        print('Permission error')
        await ctx.message.add_reaction('🚫')
        return
    raise error

@functions.utils.admin()
@bot.command()
async def cogs(ctx, action, cog):
    try:
        if action == "load":
            message = await ctx.send(embed=discord.Embed(title=f'Loading {cog}...', description=''))
            bot.load_extension(f'cogs.{cog}')
            await message.edit(embed=discord.Embed(title=f'{cog} loaded.', description='', color=0xFF0000))
        elif action == "unload":
            message = await ctx.send(embed=discord.Embed(title=f'Unloading {cog}...', description=''))
            bot.unload_extension(f'cogs.{cog}')
            await message.edit(embed=discord.Embed(title=f'{cog} unloaded.', description='', color=0xFF0000))
        elif action == "reload":
            if cog != "all":
                message = await ctx.send(embed=discord.Embed(title=f'Reloading {cog}...', description=''))
                bot.reload_extension(f'cogs.{cog}')
                await message.edit(embed=discord.Embed(title=f'{cog} reloaded.', description='', color=0xFF0000))
            else:
                message = await ctx.send(embed=discord.Embed(title=f'Reloading all cogs...', description=''))
                fileAmount = len(os.listdir('./cogs'))
                i = 0
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        i = i + 1
                        bot.reload_extension(f"cogs.{filename[:-3]}")
                    if i % 5 == 0:
                        await message.edit(embed=discord.Embed(title=f'{i} cogs reloaded.'))
                await message.edit(embed=discord.Embed(title=f'All {i} cogs reloaded.', description='', color=0xFF0000))
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(embed=discord.Embed(title=f'{cog} is already loaded.'))
    except commands.ExtensionNotLoaded:
        await ctx.send(embed=discord.Embed(title=f'{cog} is not loaded.'))
    except commands.ExtensionNotFound:
        await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))

@functions.utils.banned()
@bot.command()
async def coglist(ctx):
    fileAmount = len(os.listdir('./cogs'))
    cogList = ""
    i = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            i += 1
            cogList = cogList + f"{filename[:-3]}, "
    await ctx.send(embed=discord.Embed(title=f'{i} cogs', description=cogList[:-2], color=0xFF0000))

@functions.utils.admin()
@bot.command()
async def shutdown(ctx):
  await ctx.send(embed=discord.Embed(title='Shutting down...', description='', color=0x0000FF))
  os.system('python3 fallback.py &')
  sys.exit(0)

try:
  config = configparser.ConfigParser()
  config.read('cred.ini')
except:
  print('cred.ini does not exist.')
  sys.exit()
# cred stands for credidentials
# i changed from env to ini so i can host the bot on raspberry pi

bot.run(config['config']['fessortoken'])
