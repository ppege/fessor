import discord
from discord.ext import commands
import functions.utils
import configparser

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @commands.command()
    async def blacklist(self, ctx, *args):
      config = configparser.ConfigParser()
      config.read('configs/config.ini')
      oldCfg = config['blacklist']['list'].split(', ')
      output = "Error"
      if len(args) == 0:
        output = config['blacklist']['list']
        await ctx.send(embed=discord.Embed(title="Blacklist", description=output))
        return
      else:
        if args[0] == "add":
          oldCfg.append(args[1])
          output = "Successfully added %s to the blacklist!" % (args[1])
        if args[0] == "remove":
          oldCfg.remove(args[1])
          output = "Successfully removed %s from the blacklist!" % (args[1])
      newCfg = ', '.join(oldCfg)
      config['blacklist']['list'] = newCfg
      with open('configs/config.ini', 'w') as configfile:
        config.write(configfile)
      embed=discord.Embed(title=output, description="", color=0xFF0000)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Blacklist(bot))
