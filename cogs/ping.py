import discord
from discord.ext import commands
import functions.utils

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def ping(self, ctx):
        ping = self.bot.latency * 1000
        ping = '{0:.5g}'.format(ping)
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"Latency: {ping} milliseconds", color=0xFF0000))

def setup(bot):
    bot.add_cog(Ping(bot))
