import discord
from discord.ext import commands
import functions.utils
import subprocess

class Devtools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @commands.command()
    async def exec(self, ctx, *, command):
        output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
        await ctx.send(f'```\n{output}\n```')

def setup(bot):
    bot.add_cog(Devtools(bot))
