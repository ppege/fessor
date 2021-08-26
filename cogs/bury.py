"""This cog adds the bury command. The command sends a bunch of newlines and a zero-width non-joiner to clean the chat without destruction""" # pylint: disable=line-too-long
from discord.ext import commands
import functions.utils # pylint: disable=import-error
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Bury(commands.Cog):
    """Bury cog"""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="bury",
                        description="Buries the chat!",
                        guild_ids=functions.utils.servers,
                        default_permission=False,
                        permissions=functions.utils.slPerms("bury"),
                        options=[
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                                )
                            ]
                        )
    async def bury(self, ctx: discord_slash.SlashContext, **kwargs):
        """The bury command sends newlines to clean chat"""
        ephemeral=functions.utils.eCheck(**kwargs)
        bury = '‌\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n‌' # pylint: disable=line-too-long
        await ctx.send(content=bury, hidden=ephemeral)

def setup(bot):
    """Adds the cog"""
    bot.add_cog(Bury(bot))
