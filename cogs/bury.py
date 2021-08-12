import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext

class Bury(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.bury()
    @cog_ext.cog_slash(name="bury", description="Buries the chat!", guild_ids=functions.utils.servers)
    async def bury(self, ctx: discord_slash.SlashContext):
      await ctx.send('‌\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n‌')

def setup(bot):
    bot.add_cog(Bury(bot))
