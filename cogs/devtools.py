import discord
from discord.ext import commands
import functions.utils
import subprocess
import git
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

class Devtools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="execute",
                        description="Executes a command on the host system",
                        guild_ids=functions.utils.servers,
                        options=[
                            create_option(
                                name="command",
                                description="the command to execute",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ],
                        default_permission=False, 
                        permissions=functions.utils.slPerms("dev")
                    )
    async def exec(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        output = subprocess.run(kwargs["command"], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
        await ctx.send(f'```\n{output}\n```', hidden = ephemeral)

    @cog_ext.cog_slash(name="update",
                        description="Updates the bot",
                        guild_ids=functions.utils.servers,
                        default_permission=False,
                        options=[
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ],
                        permissions=functions.utils.slPerms("dev")
                    )
    async def update(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        repo = git.Repo()
        remote = repo.remotes.origin
        await ctx.defer(hidden=ephemeral)
        remote.pull()
        await ctx.send(embed=discord.Embed(title='Bot updated.', color=0xFF0000))

def setup(bot):
    bot.add_cog(Devtools(bot))
