"""Adds several developer tools, only usable by users with IDs in permissions.json's devlist."""
import subprocess
import discord
from discord.ext import commands
import git
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import functions.utils # pylint: disable=import-error

class Devtools(commands.Cog):

    """Devtools cog."""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="execute",
        description="Executes a command on the host system",
        guild_ids=functions.utils.servers,
        options=[
            create_option(
                name="command",
                description="the command to execute",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption,
        default_permission=False,
        permissions=functions.utils.slash_perms("dev")
    )
    async def exec(self, ctx: discord_slash.SlashContext, **kwargs):
        """Execute command line commands on the host device."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        await ctx.defer(hidden=ephemeral)
        output = subprocess.check_output(kwargs["command"], stderr=subprocess.STDOUT, shell=True, timeout=20)
        output = output.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')[2:-1]
        await ctx.send(f'```\n{output}\n```', hidden=ephemeral)

    @cog_ext.cog_slash(
        name="update",
        description="Updates the bot",
        guild_ids=functions.utils.servers,
        default_permission=False,
        options=functions.utils.privateOption,
        permissions=functions.utils.slash_perms("dev")
    )
    async def update(self, ctx: discord_slash.SlashContext, **kwargs):
        """Use git pull to update the bot."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        repo = git.Repo()
        remote = repo.remotes.origin
        await ctx.defer(hidden=ephemeral)
        remote.pull()
        await ctx.send(embed=discord.Embed(title='Bot updated.', color=0xFF0000))

def setup(bot):
    """Adds the cog."""
    bot.add_cog(Devtools(bot))
