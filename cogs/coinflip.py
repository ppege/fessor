import discord
from discord.ext import commands
import random

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cf', 'flip'])
    async def coinflip(self, ctx):
        def getResult():
            result = random.uniform(0, 1)
            if result > 0.5:
                output = "Heads!"
            else:
                output = "Tails!"
            return output, result
        output, result = getResult()
        message = await ctx.send(embed=discord.Embed(title=output, description=f"Float: {str(result)}", color=0xFF0000))
        await message.add_reaction('🔄')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🔄'

        while(True):
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            output, result = getResult()
            await message.edit(embed=discord.Embed(title=output, description=f"Float: {str(result)}", color=0xFF0000))

def setup(bot):
    bot.add_cog(Coinflip(bot))
