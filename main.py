#print('importing libraries...')
import sys
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
#print('importing modules...')
from keep_alive import keep_alive
from functions.school import schedule
from functions.school.lektiescanner import lektiescan


client = discord.Client()

@client.event
async def on_ready():
  print('MAIN READY')
  await client.change_presence(activity=discord.Game(name="test!!!"))
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  if any(word in message.content.lower() for word in config['blacklist']['list'].split(', ')):
    try:
      await message.delete()
    except:
      await message.add_reaction('🇱')
  if message.author.id == 159985870458322944:
    await message.channel.send('Luk røven MEE6')
  if message.content == ".shutdown" and config[str(message.author.id)]['admin'] == "true":
    sys.exit()
  if message.content == "pingmain":
    print('main pinged')
    await message.channel.send('pongmain')



keep_alive()
#print('logging in...')
client.run(os.getenv('fessortoken'))
