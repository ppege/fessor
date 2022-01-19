"""Adds a romkugle command."""
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import functions.utils # pylint: disable=import-error

class Romkugle(commands.Cog):
    """The romkugle cog."""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="romkugler",
        description="Hvor mange romkugler er der i denne mængde kroner??",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="kroner",
                description="hvor mange kroner?",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption
    )
    async def ping(self, ctx: discord_slash.SlashContext, **kwargs):
        """The romkugle command, returns the amount of romkuglers you can buy."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        rom = kwargs["kroner"]/10
        await ctx.send(embed=discord.Embed(title="Romkugler", description=f"Du kan købe {rom} romkugler for {kwargs['kroner']}", color=0xFF0000), hidden=ephemeral)

def setup(bot):
    """Adds the cog."""
    bot.add_cog(Romkugle(bot))
