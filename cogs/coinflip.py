import discord
from discord.ext import commands
import random

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx):
        result = random.uniform(0, 1)
        if result > 0.5:
            output = "Heads!"
        else:
            output = "Tails!"
        await ctx.send(embed=discord.Embed(title=output, description=f"Float: {str(result)}", color=0xFF0000))

def setup(bot):
    bot.add_cog(Coinflip(bot))
