import discord
from discord.ext import commands
import functions.utils

class Bury(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.bury()
    @commands.command()
    async def bury(self, ctx):
      await ctx.send('‌\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n‌')

def setup(bot):
    bot.add_cog(Bury(bot))
