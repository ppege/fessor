import discord
from discord.ext import commands
import git
import configparser
import json
import time
import platform
import functions.utils
import datetime

config = configparser.ConfigParser()
config.read('cred.ini')

if config['config']['mode'] == "updates":
  prefix = ','
else:
  prefix = '.'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print('control ready')
    

    async def sendMessage(channel, message):
        await channel.send(message)

    
    async def control():
        while(True):
            message = input()
            guild = bot.get_guild(799253855677579285)
            channel = guild.get_channel(816691188908294205)
            try:
                await sendMessage(channel, message)
            except:
                continue
    
    await control()

try:
  config = configparser.ConfigParser()
  config.read('cred.ini')
except:
  print('cred.ini does not exist.')
  sys.exit()
# cred stands for credidentials
# i changed from env to ini so i can host the bot on raspberry pi

bot.run(config['config']['fessortoken'])
