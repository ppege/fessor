import discord
from discord.ext import commands
import functions.utils

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.settings()
    @commands.command()
    async def settings(self, ctx, setting, value):
      try:
        if setting not in options.settings or value not in options.values:
          embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
          embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
          await ctx.send(embed=embed)
        else:
          config = configparser.ConfigParser()
          config.read('configs/config.ini')
          config['config'][setting] = value
          with open('configs/config.ini', 'w') as configfile:
            config.write(configfile)
          output = setting + "has been set to " + value
          embed=discord.Embed(title=output, description="", color=0xFF0000)
      except:
        embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
        embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Settings(bot))
