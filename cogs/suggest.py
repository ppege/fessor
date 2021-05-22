import discord
from discord.ext import commands
import functions.utils

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def suggest(self, ctx, suggestion):
      f = open("suggestions.md", "a")
      content = "\n## Suggestion from %s\n- %s" % (ctx.author, suggestion)
      f.write(content)
      f.close()
      user = self.bot.get_user(273845229130481665)
      await user.send(embed=discord.Embed(title='Suggestion from %s' % ctx.author, description=suggestion, color=0xFF0000))
      await ctx.send(embed=discord.Embed(title='Suggestion sendt', description=suggestion, color=0xFF0000))

def setup(bot):
    bot.add_cog(Status(bot))
