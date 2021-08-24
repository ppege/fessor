import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Bury(commands.Cog):
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
        ephemeral=functions.utils.eCheck(**kwargs)
        bury = '‌\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n‌'
        await ctx.send(content=bury, hidden=ephemeral)

def setup(bot):
    bot.add_cog(Bury(bot))
