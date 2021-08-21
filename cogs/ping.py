import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping",
                        description="Ping the bot",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
                        options=[
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def ping(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        ping = self.bot.latency * 1000
        ping = '{0:.5g}'.format(ping)
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"Latency: {ping} milliseconds", color=0xFF0000), hidden=ephemeral)

def setup(bot):
    bot.add_cog(Ping(bot))
