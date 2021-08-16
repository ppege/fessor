import discord
from discord.ext import commands
import git
import configparser
import json
import time
import platform
import functions.utils
import datetime
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getUptime(self):
        with open("data/data.json", "r") as file:
            data = json.load(file)
        uptime = time.time() - data['startTime']
        return str(datetime.timedelta(seconds=uptime))

    @functions.utils.banned()
    @cog_ext.cog_slash(name="info",
                        description="Bot statistics",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("banned"),
                        options=[
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def info(self, ctx: discord_slash.SlashContext, **kwargs):
        serverCount = len(self.bot.guilds)
        ping = self.bot.latency * 1000
        config = configparser.ConfigParser()
        config.read('cred.ini')
        with open("data/data.json", "r") as file:
          data = json.load(file)
        uptime = self.getUptime()
        my_system = platform.uname()
        repo = git.Repo()
        count = repo.git.rev_list('--count', 'HEAD')
        description = f"Servers: `{serverCount}`\nSystem: `{my_system.node} (running {my_system.system})`\nExact ping: `{ping}`\nUptime: `{uptime}`\nUses: `{data['useCount']}`\nMode: `{config['config']['mode']}`\nVersion: `{count}`"
        embed=discord.Embed(title='Information and statistics', description=description, color=0x000143)
        embed.add_field(name='Latest changes', value=repo.head.commit.message)
        embed.set_footer(text='Created and maintained by Nangu')
        if len(kwargs) == 0:
            await ctx.send(embed=embed, hidden=True)
        else:
            if kwargs["private"] == False:
                await ctx.send(embed=embed, hidden=False)
            else:
                await ctx.send(embed=embed, hidden=True)
def setup(bot):
    bot.add_cog(Info(bot))
