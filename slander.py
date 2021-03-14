import discord
import os
import schedule
import datetime
from threading import Timer
import pytz
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
import asyncio
import file
import lektiescanner

client = discord.Client()
bot = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
  print('Slander module has been loaded on {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  f = open("config.py", "r")
  config = f.read()
  f.close()
  if "autoslander = False" in config and !message.content.startswith("."):
    return
  input = message.content.replace('.', '')
  