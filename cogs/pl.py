import discord
from discord.ext import commands
import functions.utils
import configparser

class Pl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def pl(self, ctx, arg):
      config = configparser.ConfigParser()
      config.read('configs/config.ini')
      await ctx.send(config['playlists'][arg])

def setup(bot):
    bot.add_cog(Pl(bot))
