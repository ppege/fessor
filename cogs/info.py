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

    @staticmethod
    def get_uptime():
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
        embed = discord.Embed(
            title='Information and statistics',
            description="Some statistics about fessor",
            color=0x000143
        )

        embed.add_field(
            name='Version',
            value=f"`{repo.git.describe()}`\n"
        )
        embed.add_field(
            name='Exact ping',
            value=f"`{self.bot.latency * 1000}`\n"
        )
        embed.add_field(
            name='Uptime',
            value=f"`{self.get_uptime()}`\n"
        )
        embed.add_field(
            name='Servers',
            value=f"`{len(self.bot.guilds)}`\n"
        )
        embed.add_field(
            name='System',
            value=f"`{platform.uname().node} (running {platform.uname().system})`\n"
        )
        embed.add_field(
            name='HEAD',
            value=f"[{str(repo.head.commit)[:7]}](https://github.com/NanguRepo/fessor/commit/{repo.head.commit})"
        )
        embed.set_footer(text='Created and maintained by Nangu', icon_url='https://avatars.githubusercontent.com/u/56510257')
        await ctx.send(embed=embed, hidden=ephemeral)
def setup(bot):
    """Adds the cog."""
    bot.add_cog(Info(bot))
