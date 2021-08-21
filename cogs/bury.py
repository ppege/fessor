import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

class Bury(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="bury", description="Buries the chat!", guild_ids=functions.utils.servers, default_permission=False, permissions=functions.utils.slPerms("bury"))
    async def bury(self, ctx: discord_slash.SlashContext):
      await ctx.send('‌\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n‌')

def setup(bot):
    bot.add_cog(Bury(bot))
