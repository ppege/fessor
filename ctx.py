from base64 import decodebytes
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from discord.utils import get
import os
import discord
import discord.ext.commands
from discord.ext.commands import CommandNotFound
import asyncio
from discord_slash.utils.manage_commands import create_option
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
import discord_slash
import subprocess

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

prefix = ',' if config['config']['mode'] == "updates" else '.'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
slash = discord_slash.SlashCommand(bot, sync_commands=True)

bot.remove_command('help')

#logging commands
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
  await bot.change_presence(activity=discord.Game(name="2169 lines of code"))


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


@slash.subcommand(base="cogs", name="load", description="Load a cog", base_default_permission=False, base_permissions=functions.utils.slPerms("dev"), guild_ids=functions.utils.servers)
async def _cogs_load(ctx: discord_slash.SlashContext, cog):
  try:
    await ctx.defer()
    bot.load_extension(f'cogs.{cog}')
    await ctx.send(embed=discord.Embed(title=f'{cog} loaded.', description='', color=0xFF0000))
  
  except commands.ExtensionAlreadyLoaded:
      await ctx.send(embed=discord.Embed(title=f'{cog} is already loaded.'))
  
  except commands.ExtensionNotFound:
      await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))

@slash.subcommand(base="cogs", name="unload", description="Unload a cog", guild_ids=functions.utils.servers)
async def _cogs_unload(ctx: discord_slash.SlashContext, cog):
  try:
    await ctx.defer()
    bot.unload_extension(f'cogs.{cog}')
    await ctx.send(embed=discord.Embed(title=f'{cog} unloaded.', description='', color=0xFF0000))

  except commands.ExtensionNotLoaded:
      await ctx.send(embed=discord.Embed(title=f'{cog} is not loaded.'))
  
  except commands.ExtensionNotFound:
      await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))
        
@slash.subcommand(base="cogs", name="reload", description="Reload a cog", guild_ids=functions.utils.servers)
async def _cogs_reload(ctx: discord_slash.SlashContext, cog):
  try:
    if cog != "all":
        await ctx.defer()
        bot.reload_extension(f'cogs.{cog}')
        await ctx.send(embed=discord.Embed(title=f'{cog} reloaded.', description='', color=0xFF0000))
    else:
        await ctx.defer()
        i = len(os.listdir('./cogs'))
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.reload_extension(f"cogs.{filename[:-3]}")
        await ctx.send(embed=discord.Embed(title=f'All {i} cogs reloaded.', description='', color=0xFF0000))
  
  except commands.ExtensionNotLoaded:
      await ctx.send(embed=discord.Embed(title=f'{cog} is not loaded.'))

  except commands.ExtensionNotFound:
      await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))

@slash.subcommand(base="cogs", name="list", description="List of all cogs", guild_ids=functions.utils.servers)
async def _cogs_list(ctx: discord_slash.SlashContext):
    fileAmount = len(os.listdir('./cogs'))
    cogList = ""
    i = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            i += 1
            cogList += f"{filename[:-3]}, "
    await ctx.send(embed=discord.Embed(title=f'{i} cogs', description=cogList[:-2], color=0xFF0000))

@slash.slash(name="shutdown", description="Shuts down the bot.", default_permission=False, permissions=functions.utils.slPerms("dev"), guild_ids=functions.utils.servers, options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
async def shutdown(ctx: discord_slash.SlashContext, **kwargs):
  ephemeral=functions.utils.eCheck(**kwargs)
  await ctx.defer(hidden=ephemeral)
  fprefix = random.choice(['$', '%', '=', '+', '^', '---', '___', '>', '>>>'])
  subprocess.Popen(['python3', 'fallback.py', fprefix])
  await ctx.send(embed=discord.Embed(title='Bot has shut down.', description=f'Fallback prefix: {fprefix}', color=0x0000FF))
  sys.exit(0)

@slash.slash(name="restart", description="Restarts the bot.", default_permission=False, permissions=functions.utils.slPerms("dev"), guild_ids=functions.utils.servers, options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
async def restart(ctx: discord_slash.SlashContext, **kwargs):
  ephemeral=functions.utils.eCheck(**kwargs)
  await ctx.defer(hidden=ephemeral)
  message = await ctx.send(embed=discord.Embed(title='Restarting...', color=0x0000FF))
  subprocess.Popen(['python3', 'fallback.py', 'restart', str(message.channel.id)])
  sys.exit(0)

try:
  config = configparser.ConfigParser()
  config.read('cred.ini')
except:
  print('cred.ini does not exist.')
  sys.exit()
# cred stands for credidentials
# i changed from env to ini so i can host the bot on raspberry pi
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f"cogs.{filename[:-3]}")
bot.run(config['config']['fessortoken'])
