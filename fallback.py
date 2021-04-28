import discord
import os
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
  print('FALLBACK READY.')

@bot.command()
async def start(ctx):
  if ctx.author.id == 273845229130481665:
    await ctx.send(embed=discord.Embed(title='Starting bot...', description='', color=0xFFFFFF)
    os.system('python3 ctx.py & python3 main.py')

@bot.command()
async def update(ctx):
  if ctx.author.id == 273845229130481665:
    await ctx.send(embed=discord.Embed(title='Updating bot...', description='', color=0xFF0000))
    os.system('git pull')

@bot.command()
async def ping(ctx):
  print('fallback pinged')
  await ctx.send('pong!')

bot.run(os.getenv('fessortoken'))
