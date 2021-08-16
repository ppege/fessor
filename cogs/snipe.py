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

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print("message deleted")
        self.snipeMessage = message

    @functions.utils.banned()
    @cog_ext.cog_slash(name="snipe",
                        description="Snipe a message that has been deleted",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("banned"),
                        options=[
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def snipe(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.eCheck(**kwargs)
        embed=discord.Embed(title=f"Sniped!", description=f"Sent at {self.snipeMessage.created_at + datetime.timedelta(hours=2)} by {self.snipeMessage.author.mention}", color=0x00FFFF)
        embed.add_field(name=f"Message content", value=self.snipeMessage.content)
        await ctx.send(embed=embed, hidden=ephemeral)


def setup(bot):
    bot.add_cog(Snipe(bot))
