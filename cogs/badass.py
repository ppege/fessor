import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

class Badass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @cog_ext.cog_slash(name="badass", description="😎", guild_ids=functions.utils.servers, permissions=functions.utils.slPerms("banned"))
    async def badass(self, ctx: discord_slash.SlashContext):
      await ctx.send('https://imgur.com/a/QqFEkrm')

def setup(bot):
    bot.add_cog(Badass(bot))
