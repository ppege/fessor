import discord
from discord.ext import commands
import functions.utils
import json
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @cog_ext.cog_slash(name="perms",
                        description="Setup permissions",
                        guild_ids=[811552770074738688],
                        options=[
                            create_option(
                                name="action",
                                description="what to do?",
                                option_type=3,
                                required=True,
                                choices=[
                                    create_choice(
                                        name="setup",
                                        value=""
                                    )
                                ]
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def perms(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)


def setup(bot):
#    bot.add_cog(Perms(bot))
    print("hi")
