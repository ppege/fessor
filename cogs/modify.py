"""This cog adds the modify command, which devs can use to modify the assets file."""
# pylint: disable=line-too-long, unspecified-encoding
import json
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import functions.utils # pylint: disable=import-error

class Modify(commands.Cog):
    """Modify cog."""
    def __init__(self, bot):
        self.bot = bot

    with open("configs/assets.json", "r") as file:
        data = json.load(file)

    @cog_ext.cog_slash(name="modify",
                        description="Modify the link registry",
                        guild_ids=functions.utils.servers,
                        default_permission=False,
                        permissions=functions.utils.slash_perms("dev"),
                        options=[
                            create_option(
                                name="category",
                                description="which category to change?",
                                option_type=3,
                                required=True,
                                choices=[
                                    create_choice(name=key, value=key) for key in data.keys()
                                ]
                            ),
                            create_option(
                                name="key",
                                description="which key to change?",
                                option_type=3,
                                required=True,
                                choices=[
                                    create_choice(name=key, value=key) for key in data["teachers"].keys()
                                ]
                            ),
                            create_option(
                                name="value",
                                description="which value to change?",
                                option_type=3,
                                required=True
                            )
                        ] + functions.utils.privateOption
                    )
    async def modify(self, ctx: discord_slash.SlashContext, **kwargs):
        """The modify command, used to modify the file lektiescanner uses to figure out which thumbnails to use."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        self.data[kwargs["category"]][kwargs["key"]] = kwargs["value"]
        with open('configs/assets.json', 'w') as file:
            json.dump(self.data, file, indent=4)
        output = "Successfully replaced"
        embed=discord.Embed(title=output, description="", color=0xFF0000)
        await ctx.send(embed=embed, hidden=ephemeral)

def setup(bot):
    """Adds the cog."""
    bot.add_cog(Modify(bot))
