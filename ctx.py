from discord.ext import commands
from discord.utils import get
import os
import discord
import discord.ext.commands
import asyncio
import os,sys,inspect
from functions.fun.slander import slander
from configs import options
import configparser

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
  print('READY.')
  print('{0.user}'.format(bot))


@bot.command()
async def s(ctx, victim):
  try:
    output = slander[victim]
    await ctx.send(output)
  except:
    embed=discord.Embed(title="Slander fejl", description="Dette slander findes ikke\nListe af slander:\n`william`\n`noah`\n`jeppe`\n`mads`\n`jakob`\n`peter`\n`asger`\n`frederik`\n`emil`\n`simon`", color=0xFF0000)
    await ctx.send(embed=embed)

@bot.command()
async def settings(ctx, setting, value):
  try:
    if setting not in options.settings or value not in options.values:
      embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
      embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
      await ctx.send(embed=embed)
    else:
      config = configparser.ConfigParser()
      config.read('configs/config.ini')
      config['config'][setting] = value
      with open('configs/config.ini', 'w') as configfile:
        config.write(configfile)
      output = setting + "has been set to " + value
      embed=discord.Embed(title=output, description="", color=0xFF0000)
  except:
    embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
    embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def bury(ctx):
  for i in range(0, 6):
    await ctx.send('https://i.imgur.com/SL9KqwC.png')

@bot.command()
async def poggies(ctx):
  f = open("poggers.txt", "r")
  fileContent = f.read()
  output = fileContent.split('\n')
  for i in range(0, len(output)):
    await ctx.send(output[i])

@bot.command()
async def badass(ctx):
  await ctx.send('https://imgur.com/a/QqFEkrm')

bot.run(os.getenv('fessortoken'))
