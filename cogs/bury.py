"""Adds the bury command. The command sends a bunch of newlines and a zero-width non-joiner to clean the chat without destruction."""
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import functions.utils # pylint: disable=import-error

class Bury(commands.Cog):
    """Bury cog."""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="bury",
        description="Buries the chat!",
        guild_ids=functions.utils.servers,
        default_permission=False,
        permissions=functions.utils.slash_perms("bury"),
        options=[
            create_option(
                name="lines",
                description="the amount of empty lines to generate. default is 35",
                option_type=3,
                required=False
            )
        ] + functions.utils.privateOption
    )
    async def bury(self, ctx: discord_slash.SlashContext, **kwargs):
        """The bury command sends newlines to clean chat."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        bury = "‌" + ("\n" * int(kwargs.get('lines') or "35")) + "‌"
        await ctx.send(content=bury, hidden=ephemeral)

def setup(bot):
    """Adds the cog."""
    bot.add_cog(Bury(bot))
