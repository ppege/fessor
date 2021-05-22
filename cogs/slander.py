import discord
from discord.ext import commands
from functions.fun.slander import slander
import functions.utils

class Slander(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.slander()
    @commands.command(aliases=['s', 'sl'])
    async def slander(self, ctx, victim):
        try:
          output = slander[victim]
          await ctx.send(output)
        except:
          embed=discord.Embed(title="Slander fejl", description="Dette slander findes ikke\nListe af slander:\n`william`\n`noah`\n`jeppe`\n`mads`\n`jakob`\n`peter`\n`asger`\n`frederik`\n`emil`\n`simon`", color=0xFF0000)
          await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slander(bot))
