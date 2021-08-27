"""This cog adds commands related to permissions"""
# pylint: disable=line-too-long, unspecified-encoding
import json
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import functions.utils # pylint: disable=import-error

class Perms(commands.Cog):
    """The perms cog"""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="perms",
                        description="Setup permissions",
                        guild_ids=functions.utils.servers,
                        default_permission=False,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="user",
                                description="which users permissions to change",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="permission",
                                description="which permission to change",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="value",
                                description="what to change the permission to",
                                option_type=3,
                                required=True,
                                choices=[
                                    create_choice(
                                        name="true",
                                        value="true"
                                    ),
                                    create_choice(
                                        name="false",
                                        value="false"
                                    )
                                ]
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def perms(self, ctx: discord_slash.SlashContext, **kwargs):
        """Command to change a given user's permissions related to the bot"""
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.defer(hidden=ephemeral)
        with open("configs/permissions.json", "r") as file:
            data = json.load(file)
        guild_id = str(ctx.guild.id)
        permission = kwargs["permission"]
        user = kwargs["user"]
        value = kwargs["value"]
        user_id = str(user.id)
        if value == "true":
            if user_id not in data[guild_id][permission]:
                data[guild_id][permission].append(user_id)
        elif user_id in data[guild_id][permission]:
            data[guild_id][permission].remove(user_id)
        data[guild_id][user_id][permission] = value

        with open("configs/permissions.json", "w") as file:
            json.dump(data, file, indent=4)
        await ctx.send(embed=discord.Embed(title="Permission changed."))

    @cog_ext.cog_slash(name="setupperms",
                        description="Setup permissions, THIS RESETS ALL PERMS",
                        guild_ids=functions.utils.servers,
                        default_permission=False,
                        permissions=functions.utils.slPerms("dev"),
                        options=[
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def setup_perms(self, ctx: discord_slash.SlashContext, **kwargs):
        """Command to setup all perms for a guild"""
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.defer(hidden=ephemeral)
        with open("configs/permissions.json", "r") as file:
            data = json.load(file)
        guild_id = ctx.guild.id
        guild = self.bot.get_guild(guild_id)
        guild_id = str(guild_id)
        try:
            data.pop(guild_id)
        except KeyError:
            pass
        data[guild_id] = {}
        ids = [member.id for member in guild.members]
        data[guild_id]["admin"] = []
        data[guild_id]["poggies"] = []
        data[guild_id]["lektiescan"] = []
        data[guild_id]["banned"] = []
        data[guild_id]["bury"] = []
        for member_id in ids:
            data[guild_id][member_id] = {
                "admin": "false",
                "poggies": "false",
                "lektiescan": "false",
                "banned": "false",
                "bury": "false"
            }
        with open("configs/permissions.json", "w") as file:
            json.dump(data, file, indent=4)
        await ctx.send(embed=discord.Embed(title="Permissions have been set up."))

def setup(bot):
    """Adds the cog"""
    bot.add_cog(Perms(bot))
