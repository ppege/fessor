"""Ran when main.py recieves the shutdown or restart command, it handles user ability to start the bot again."""
import sys
import subprocess
import configparser
import discord
from discord.ext import commands

prefix = sys.argv[1] if sys.argv[1] != "restart" else "$"
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    """Things that happen when the bot is ready."""
    print('FALLBACK READY.')
    print(sys.argv)
    if sys.argv[1] == "restart":
        subprocess.Popen(['python3', 'main.py'])
        channel = bot.get_channel(int(sys.argv[2]))
        await channel.send(embed=discord.Embed(title='Bot started.', color=0xFF0000))
        sys.exit(0)

@bot.command()
async def start(ctx):
    """Command to start the bot again."""
    if ctx.author.id == 273845229130481665:
        message = await ctx.send(embed=discord.Embed(title='Starting bot...', description='', color=0xFFFFFF))
        subprocess.Popen(['python3', 'main.py'])
        await message.edit(embed=discord.Embed(title='Bot started.', description='', color=0xFF0000))
        sys.exit(0)

@bot.command()
async def ping(ctx):
    """Ping command so the user can see if the script is running."""
    await ctx.send('pong!')

config = configparser.ConfigParser()
config.read('cred.ini')
bot.run(config['config']['fessortoken'])
