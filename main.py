import discord
import os
import datetime
import configparser
from threading import Timer
import pytz
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
import asyncio
import file
from school import schedule
print('importing lektiescanner')
from school.lektiescanner import lektiescan
print('finished importing lektiescanner')


client = discord.Client()
bot = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="gaming"))
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  config = configparser.ConfigParser()
  config.read('configs/config.ini')






beskrivelse, begivenhed, tidspunkt, files, fileNames, author = lektiescan()
print(beskrivelse[0])




keep_alive()
client.run(os.getenv('fessortoken'))