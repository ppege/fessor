"""The main file that should be launched to start the bot; loads all cogs and logs in to the bot."""
import os
import datetime
import sys
import configparser
import time
import random
import json
import subprocess
from glob import glob
from discord.ext import commands
import discord
from discord.ext.commands import CommandNotFound
from pygount import ProjectSummary, SourceAnalysis
import discord_slash
from discord_slash.utils.manage_commands import create_option
import functions.utils

startTime = time.time()
try:
    with open("data/data.json", "r") as file:
        DATA = json.load(file)
except FileNotFoundError:
    with open("data/data.json", "w+") as file:
        DATA={}
        DATA['startTime'] = startTime
        json.dump(DATA, file, indent=4)
with open("data/data.json", "w") as file:
    DATA['startTime'] = startTime
    json.dump(DATA, file, indent=4)
def get_uptime():
    """Get bot uptime by subtracting start time from current time."""
    uptime = time.time() - startTime
    return str(datetime.timedelta(seconds=uptime))

config = configparser.ConfigParser()
config.read('cred.ini')

try:
    PREFIX = ',' if config['config']['mode'] == "updates" else '.'
except KeyError:
    print("cred.ini does not exist yet")
    sys.exit(1)
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
slash = discord_slash.SlashCommand(bot, sync_commands=True)

bot.remove_command('help')

#logging commands
@bot.event
async def on_command(ctx):
    """Logs command use; this function is currently unused."""
    with open("data/log.txt", "a") as log:
        log.write(f"[{datetime.datetime.now()}] {ctx.author}: \"{ctx.message.content}\" | Message ID: {ctx.message.id} | Author ID: {ctx.author.id}\n")
    with open("data/data.json", "r") as json_file:
        json_data = json.load(json_file)
    try:
        json_data['useCount'] = json_data['useCount'] + 1
    except KeyError:
        json_data['useCount'] = 1
    json_data['lastUse'] = str(datetime.datetime.now())
    json_data['lastCommandUsed'] = ctx.message.content
    with open("data/data.json", "w") as json_file:
        json.dump(json_data, json_file)

@bot.event
async def on_ready():
    """Executed once the bot is ready."""
    print('fessor is online.')
    project_summary = ProjectSummary()
    source_paths = glob("**/*.py", recursive=True)
    for source_path in source_paths:
        source_analysis = SourceAnalysis.from_file(source_path, "pygount")
        project_summary.add(source_analysis)
    await bot.change_presence(activity=discord.Game(name=f"{project_summary.total_line_count} lines of code"))


@bot.event
async def on_command_error(ctx, error):
    """Command error handling; this function is not in use."""
    if isinstance(error, CommandNotFound):
        await ctx.send(embed=discord.Embed(title='Invalid kommando', description='Brug .help for en liste af kommandoer'))
        return
    if isinstance(error, commands.CheckFailure):
        print('Permission error')
        await ctx.message.add_reaction('🚫')
        return
    raise error


@slash.subcommand(base="cogs", name="load", description="Load a cog", base_default_permission=False, base_permissions=functions.utils.slash_perms("dev"), guild_ids=functions.utils.servers)
async def _cogs_load(ctx: discord_slash.SlashContext, cog):
    try:
        await ctx.defer()
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(embed=discord.Embed(title=f'{cog} loaded.', description='', color=0xFF0000))

    except commands.ExtensionAlreadyLoaded:
        await ctx.send(embed=discord.Embed(title=f'{cog} is already loaded.'))

    except commands.ExtensionNotFound:
        await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))

@slash.subcommand(base="cogs", name="unload", description="Unload a cog", guild_ids=functions.utils.servers)
async def _cogs_unload(ctx: discord_slash.SlashContext, cog):
    try:
        await ctx.defer()
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(embed=discord.Embed(title=f'{cog} unloaded.', description='', color=0xFF0000))

    except commands.ExtensionNotLoaded:
        await ctx.send(embed=discord.Embed(title=f'{cog} is not loaded.'))

    except commands.ExtensionNotFound:
        await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))

@slash.subcommand(base="cogs", name="reload", description="Reload a cog", guild_ids=functions.utils.servers)
async def _cogs_reload(ctx: discord_slash.SlashContext, cog):
    try:
        if cog != "all":
            await ctx.defer()
            bot.reload_extension(f'cogs.{cog}')
            await ctx.send(embed=discord.Embed(title=f'{cog} reloaded.', description='', color=0xFF0000))
        else:
            await ctx.defer()
            i = len(os.listdir('./cogs'))
            for file_name in os.listdir('./cogs'):
                if file_name.endswith('.py'):
                    bot.reload_extension(f"cogs.{file_name[:-3]}")
            await ctx.send(embed=discord.Embed(title=f'All {i} cogs reloaded.', description='', color=0xFF0000))

    except commands.ExtensionNotLoaded:
        await ctx.send(embed=discord.Embed(title=f'{cog} is not loaded.'))

    except commands.ExtensionNotFound:
        await ctx.send(embed=discord.Embed(title=f'Cog "{cog}" does not exist.'))

@slash.subcommand(base="cogs", name="list", description="List of all cogs", guild_ids=functions.utils.servers)
async def _cogs_list(ctx: discord_slash.SlashContext):
    i = 0
    cog_list = ""
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            i += 1
            cog_list += f"{file_name[:-3]}, "
    await ctx.send(embed=discord.Embed(title=f'{i} cogs', description=cog_list[:-2], color=0xFF0000))

@slash.slash(name="shutdown", description="Shuts down the bot.", default_permission=False, permissions=functions.utils.slash_perms("dev"), guild_ids=functions.utils.servers, options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
async def shutdown(ctx: discord_slash.SlashContext, **kwargs):
    """Command to shut down the bot. Opens a background script with a randomized prefix to let me remotely start the bot again."""
    ephemeral = functions.utils.ephemeral_check(**kwargs)
    await ctx.defer(hidden=ephemeral)
    fprefix = random.choice(['$', '%', '=', '+', '^', '---', '___', '>', '>>>'])
    subprocess.Popen(['python3', 'fallback.py', fprefix])
    await ctx.send(embed=discord.Embed(title='Bot has shut down.', description=f'Fallback prefix: {fprefix}', color=0x0000FF))
    sys.exit(0)

@slash.slash(name="restart", description="Restarts the bot.", default_permission=False, permissions=functions.utils.slash_perms("dev"), guild_ids=functions.utils.servers, options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
async def restart(ctx: discord_slash.SlashContext, **kwargs):
    """Restarts the bot by running fallback.py with the restart argument."""
    ephemeral = functions.utils.ephemeral_check(**kwargs)
    await ctx.defer(hidden=ephemeral)
    message = await ctx.send(embed=discord.Embed(title='Restarting...', color=0x0000FF))
    subprocess.Popen(['python3', 'fallback.py', 'restart', str(message.channel.id)])
    sys.exit(0)

config = configparser.ConfigParser()
config.read('cred.ini')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")
bot.run(config['config']['fessortoken'])
