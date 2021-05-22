import discord
from discord.ext import commands
import functions.utils

class Badass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def badass(self, ctx):
      await ctx.send('https://imgur.com/a/QqFEkrm')

def setup(bot):
    bot.add_cog(Badass(bot))
