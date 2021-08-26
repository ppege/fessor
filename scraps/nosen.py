import discord
import os
import configparser
from configs import birte

client = discord.Client()

config = configparser.ConfigParser()
config.read('cred.ini')

@client.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="Odio a Birte con todo mi corazón"))

@client.event
async def on_message(message):
    if message.content in birte.commands.keys():
        for i in range(len(birte.commands[message.content])):
            await message.channel.send(birte.commands[message.content][i])


client.run(config['config']['fessortoken'])