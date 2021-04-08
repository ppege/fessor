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

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='.', intents=intents)

async def notify(id, cause):
  if cause == 'banned':
    output = 'Fucking mongol, du er BANNET fra FESSOR BOT :joy:'
  elif cause == 'no':
    output = 'Du har ikke tilladelse til denne kommando IDIOT'
  else:
    output = 'Jeg ved ikke hvorfor du får denne besked, sig det til william pls'
  user = bot.get_user(id)
  await user.send(output)

async def check(id, permission):
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  allowed = "no"
  id = str(id)
  if config[id][permission] == 'true':
    allowed = "yes"
  if config[id]['banned'] == 'true':
    allowed = "banned"
  if config[id]['admin'] == 'true':
    allowed = "yes"
  if allowed != "yes":
    await notify(int(id), allowed)
  return allowed


@bot.event
async def on_ready():
  print('READY.')
  print('{0.user}'.format(bot))


@bot.command()
async def s(ctx, victim):
  allowed = await check(ctx.author.id, 'slander')
  if allowed != "yes": return
  try:
    output = slander[victim]
    await ctx.send(output)
  except:
    embed=discord.Embed(title="Slander fejl", description="Dette slander findes ikke\nListe af slander:\n`william`\n`noah`\n`jeppe`\n`mads`\n`jakob`\n`peter`\n`asger`\n`frederik`\n`emil`\n`simon`", color=0xFF0000)
    await ctx.send(embed=embed)

@bot.command()
async def settings(ctx, setting, value):
  allowed = await check(ctx.author.id, 'settings')
  if allowed != "yes": return
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
  allowed = await check(ctx.author.id, 'bury')
  if allowed != "yes": return
  for i in range(0, 6):
    await ctx.send('https://i.imgur.com/SL9KqwC.png')

@bot.command()
async def poggies(ctx):
  allowed = await check(ctx.author.id, 'poggies')
  if allowed != "yes": return
  f = open("poggers.txt", "r")
  fileContent = f.read()
  output = fileContent.split('\n')
  for i in range(0, len(output)):
    await ctx.send(output[i])

@bot.command()
async def badass(ctx):
  await ctx.send('https://imgur.com/a/QqFEkrm')

@bot.command()
async def perms(ctx, *args):
  allowed = await check(ctx.author.id, 'admin')
  if allowed != "yes": return
  if args[0] == 'reset':
    ids = [member.id for member in ctx.guild.members]
    print(str(ids))
    for i in range(0, len(ids)):
      config = configparser.ConfigParser()
      config.read('configs/config.ini')
      config[str(ids[i])] = {'admin': 'false', 'settings': 'false', 'poggies': 'true', 'lektiescan': 'true', 'banned': 'false', 'slander': 'true'}
      with open('configs/config.ini', 'w') as configfile:
        config.write(configfile)
    output = "permissions have been reset"
    embed=discord.Embed(title=output, description="", color=0xFF0000)
    await ctx.send(embed=embed)
  else:
    id = args[0].replace('<@!', '').replace('>', '')
    permission = args[1]
    value = args[2]
    config = configparser.ConfigParser()
    config.read('configs/config.ini')
    config[id][permission] = value
    with open('configs/config.ini', 'w') as configfile:
      config.write(configfile)
    output = id + "'s '" + permission + "' permission has been set to '" + value + "'"
    embed=discord.Embed(title=output, description="", color=0xFF0000)
    await ctx.send(embed=embed)

bot.run(os.getenv('petertoken'))