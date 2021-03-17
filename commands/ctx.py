from discord.ext import commands
from discord.utils import get
import os
import discord
import discord.ext.commands
import asyncio
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from fun.slander import slander

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

bot.run(os.getenv('fessortoken'))