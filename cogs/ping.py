"""This cog adds a ping command"""
# pylint: disable=line-too-long
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
import functions.utils # pylint: disable=import-error

class Ping(commands.Cog):
    """The ping cog"""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping",
                        description="Ping the bot",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slash_perms("banned"),
                        options=functions.utils.privateOption
                    )
    async def ping(self, ctx: discord_slash.SlashContext, **kwargs):
        """The ping command, returns the bot's ping"""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        ping = self.bot.latency * 1000
        ping = '{0:.5g}'.format(ping)
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"Latency: {ping} milliseconds", color=0xFF0000), hidden=ephemeral)

def setup(bot):
    """Adds the cog"""
    bot.add_cog(Ping(bot))
