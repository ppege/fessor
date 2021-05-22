import discord
from discord.ext import commands
import functions.utils
import configparser

class Modify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @commands.command()
    async def modify(self, ctx, category, key, value):
      config = configparser.ConfigParser()
      config.read('configs/assets.ini')
      config[category][key] = value
      with open('configs/assets.ini', 'w') as configfile:
        config.write(configfile)
      output = "Successfully replaced"
      embed=discord.Embed(title=output, description="", color=0xFF0000)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Modify(bot))
