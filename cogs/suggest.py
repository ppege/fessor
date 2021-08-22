import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="suggest",
                        description="Suggest a feature",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
                        options=[
                            create_option(
                                name="suggestion",
                                description="what do you suggest?",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def suggest(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        suggestion = kwargs["suggestion"]
        with open("suggestions.md", "a") as f:
            content = "\n## Suggestion from %s\n#### %s" % (ctx.author, suggestion)
            f.write(content)
        user = self.bot.get_user(273845229130481665)
        await user.send(embed=discord.Embed(title='Suggestion from %s' % ctx.author, description=suggestion, color=0xFF0000))
        await ctx.send(embed=discord.Embed(title='Suggestion sendt', description=suggestion, color=0xFF0000), hidden=ephemeral)

def setup(bot):
    bot.add_cog(Status(bot))
