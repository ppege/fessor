import discord
from discord.ext import commands
import functions.utils
import datetime
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    snipeMessage = {}
    snipeMessageEdit = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print("message deleted")
        self.snipeMessage = message
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        print("message edited")
        self.snipeMessageEdit = before

    @functions.utils.banned()
    @cog_ext.cog_slash(name="snipe",
                        description="Snipe a message that has been deleted",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("banned"),
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
        if kwargs["mode"] == "edit":
            self.snipeMessage = self.snipeMessageEdit
        embed=discord.Embed(title=f"Sniped!", description=f"Sent at {self.snipeMessage.created_at + datetime.timedelta(hours=2)} by {self.snipeMessage.author.mention}", color=0x00FFFF)
        embed.add_field(name=f"Message content", value=self.snipeMessage.content)
        if kwargs["mode"] == "edit":
            await ctx.send("Sniped", hidden=True)
            await self.snipeMessage.reply(embed=embed)
        else:
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Snipe(bot))
