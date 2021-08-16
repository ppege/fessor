import discord
from discord.ext import commands
import functions.utils
import json
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

class Modify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open("configs/assets.json", "r") as file:
        data = json.load(file)

    @functions.utils.admin()
    @cog_ext.cog_slash(name="modify",
                        description="Modify the link registry",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("dev"),
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
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def modify(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        self.data[kwargs["category"]][kwargs["key"]] = kwargs["value"]
        with open('configs/assets.json', 'w') as file:
            json.dump(self.data, file, indent=4)
        output = "Successfully replaced"
        embed=discord.Embed(title=output, description="", color=0xFF0000)
        await ctx.send(embed=embed, hidden=ephemeral)

def setup(bot):
    bot.add_cog(Modify(bot))
