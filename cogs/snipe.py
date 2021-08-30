"""Adds a snipe command, that picks up deleted or edited messages and allows the user to see what was previously there."""
import datetime
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import functions.utils # pylint: disable=import-error

class Snipe(commands.Cog):

    """The snipe cog."""
    def __init__(self, bot):
        self.bot = bot

    snipe_message = {}
    snipe_message_edit = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Picks up message deletions."""
        print("message deleted")
        self.snipe_message = message

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Picks up message edits."""
        if before.content == after.content:
            return
        print("message edited")
        self.snipe_message_edit = before

    @cog_ext.cog_slash(
        name="snipe",
        description="Snipe a message that has been deleted",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="mode",
                description="which event to catch",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="Deletion",
                        value="del"
                    ),
                    create_choice(
                        name="Edit",
                        value="edit"
                    )
                ]
            )
        ]
    )
    async def snipe(self, ctx: discord_slash.SlashContext, **kwargs):
        """The snipe command, provides the user with the option to snipe a deletion or an edit."""
        if kwargs["mode"] == "edit":
            self.snipe_message = self.snipe_message_edit
        embed = discord.Embed(
            title='Sniped!',
            description=f"Sent at {self.snipe_message.created_at + datetime.timedelta(hours=2)} by {self.snipe_message.author.mention}",
            color=0x00FFFF,
        )

        embed.add_field(name='Message content', value=self.snipe_message.content)
        if kwargs["mode"] == "edit":
            await ctx.send("Sniped", hidden=True)
            await self.snipe_message.reply(embed=embed)
        else:
            await ctx.send(embed=embed)


def setup(bot):
    """Adds the cog."""
    bot.add_cog(Snipe(bot))
