print('importing libraries...')
import discord
import os
import datetime
import configparser
from threading import Timer
import pytz
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
import asyncio
print('importing modules...')
from keep_alive import keep_alive
from functions.school import schedule
from functions.school.lektiescanner import lektiescan


client = discord.Client()

@client.event
async def on_ready():
  print('main logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name=".help"))
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  if any(word in message.content.lower() for word in config['blacklist']['list'].split(', ')):
    await message.delete()
  if message.author.id == 159985870458322944:
    await message.channel.send('Luk røven MEE6')




keep_alive()
print('logging in...')
client.run(os.getenv('fessortoken'))
