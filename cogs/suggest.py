"""Adds the suggest command, which lets the user send a suggestion for fessor."""
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import functions.utils # pylint: disable=import-error

class Suggest(commands.Cog):
    """The suggest cog."""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="suggest",
        description="Suggest a feature",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="suggestion",
                description="what do you suggest?",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption
    )
    async def suggest(self, ctx: discord_slash.SlashContext, **kwargs):
        """Command which lets the user send a suggestion to fessor."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        suggestion = kwargs["suggestion"]
        with open("suggestions.md", "a") as file:
            content = "\n## Suggestion from %s\n#### %s" % (ctx.author, suggestion)
            file.write(content)
        user = self.bot.get_user(273845229130481665)
        await user.send(embed=discord.Embed(title='Suggestion from %s' % ctx.author, description=suggestion, color=0xFF0000))
        await ctx.send(embed=discord.Embed(title='Suggestion sendt', description=suggestion, color=0xFF0000), hidden=ephemeral)

def setup(bot):
    """Adds the cog."""
    bot.add_cog(Suggest(bot))
