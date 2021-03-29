from discord.ext import commands
from discord.utils import get
import os
import discord
import discord.ext.commands
import asyncio
import os,sys,inspect
from commands.fun.slander import slander
from configs import settings
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
async def settings(ctx, arg1, arg2):
  if arg1 not in settings.arg1 or arg2 not in settings.arg2:
    embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
    embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
    ctx.send(embed=embed)
	else:
    config = configparser.ConfigParser()
    config.read('configs/config.ini')
    config['config'][arg1] = arg2

bot.run(os.getenv('fessortoken'))
