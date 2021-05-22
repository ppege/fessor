import discord
from discord.ext import commands
import git
import configparser
import json
import time
import platform
import functions.utils

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getUptime():
        print('getUptime called')
        with open("data/data.json", "r") as file:
            data = json.load(file)
        uptime = time.time() - data['startTime']
        return str(datetime.timedelta(seconds=uptime))

    @functions.utils.banned()
    @commands.command(aliases=['stats', 'status'])
    async def info(self, ctx):
        config = configparser.ConfigParser()
        config.read('cred.ini')
        with open("data/data.json", "r") as file:
          data = json.load(file)
        uptime = time.time() - data['startTime']
        my_system = platform.uname()
        repo = git.Repo()
        count = repo.git.rev_list('--count', 'HEAD')
        description = f"System: `{my_system.node} (running {my_system.system})`\nUptime: `{uptime}`\nUses: `{data['useCount']}`\nMode: `{config['config']['mode']}`\nVersion: `{count}`"
        embed=discord.Embed(title='Information and statistics', description=description, color=0x000143)
        embed.add_field(name='Latest changes', value=repo.head.commit.message)
        embed.set_footer(text='Created and maintained by Nangu')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
