"""Adds the info command that relays a bunch of statistics."""
import json
import configparser
import time
import platform
import datetime
import discord
from discord.ext import commands
import git
import discord_slash
from discord_slash import cog_ext
import functions.utils # pylint: disable=import-error

class Info(commands.Cog):
    """Info cog."""
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def get_uptime(cls):
        """Reads the start time of the bot from data.json then subtracts it from the current time."""
        with open("data/data.json", "r") as file:
            data = json.load(file)
        uptime = time.time() - data['startTime']
        return str(datetime.timedelta(seconds=uptime))

    @cog_ext.cog_slash(
        name="info",
        description="Bot statistics",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=functions.utils.privateOption
    )
    async def info(self, ctx: discord_slash.SlashContext, **kwargs):
        """The info command."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        config = configparser.ConfigParser()
        config.read('cred.ini')
        repo = git.Repo()
        description = (
            f"Version: `{repo.git.describe()}`\n"
            f"Exact ping: `{self.bot.latency * 1000}`\n"
            f"Uptime: `{self.get_uptime()}`\n"
            #f"Times used: `{data['useCount']}`\n"
            f"Servers: `{len(self.bot.guilds)}`\n"
            f"System: `{platform.uname().node} (running {platform.uname().system})`\n"
            f"Mode: `{config['config']['mode']}`"
        )
        embed = discord.Embed(
            title='Information and statistics',
            description=description,
            color=0x000143
        )
        embed.add_field(
            name='Latest changes',
            value=f"`{str(repo.head.commit)[:7]}`\n{repo.head.commit.message}"
        )
        embed.set_footer(text='Created and maintained by Nangu')
        await ctx.send(embed=embed, hidden=ephemeral)
def setup(bot):
    """Adds the cog."""
    bot.add_cog(Info(bot))
