import discord
from discord.ext import commands
import functions.utils
import subprocess
import git
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Devtools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @cog_ext.cog_slash(name="execute",
                        description="Executes a command on the host system",
                        guild_ids=functions.utils.servers,
                        options=[
                            create_option(
                                name="ephemeral",
                                description="send the output privately",
                                option_type=5,
                                required=True
                            ),
                            create_option(
                                name="command",
                                description="the command to execute",
                                option_type=3,
                                required=True
                            )
                        ]
                    )
    async def exec(self, ctx: discord_slash.SlashContext, ephemeral, command):
        output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
        if ephemeral == True:
            await ctx.send(f'```\n{output}\n```', hidden = True)
        else:
            await ctx.send(f'```\n{output}\n```', hidden = False)

    @functions.utils.admin()
    @cog_ext.cog_slash(name="update",
                        description="Updates the bot",
                        guild_ids=functions.utils.servers)
    async def update(self, ctx: discord_slash.SlashContext):
        repo = git.Repo()
        remote = repo.remotes.origin
        message = await ctx.send(embed=discord.Embed(title='Updating bot...', description=''))
        remote.pull()
        await message.edit(embed=discord.Embed(title='Bot updated.', description='', color=0xFF0000))

def setup(bot):
    bot.add_cog(Devtools(bot))
