import discord
from discord.ext import commands
import functions.utils

class Poggies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.poggies()
    @commands.command()
    async def poggies(self, ctx):
      f = open("configs/poggers.txt", "r")
      fileContent = f.read()
      output = fileContent.split('\n')
      for i in range(0, len(output)):
        await ctx.send(output[i])


def setup(bot):
    bot.add_cog(Poggies(bot))
