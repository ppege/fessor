import discord
from discord.ext import commands
import functions.utils
import subprocess
import git

class Devtools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @commands.command()
    async def exec(self, ctx, *, command):
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
        await ctx.send(f'```\n{output}\n```')

    @functions.utils.admin()
    @commands.command()
    async def update(self, ctx):
        repo = git.Repo()
        remote = repo.remotes.origin
        message = await ctx.send(embed=discord.Embed(title='Updating bot...', description=''))
        remote.pull()
        await message.edit(embed=discord.Embed(title='Bot updated.', description='', color=0xFF0000))

def setup(bot):
    bot.add_cog(Devtools(bot))
