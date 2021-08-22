import discord
from discord.ext import commands
import functions.utils
import json
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Perms(commands.Cog):
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
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.defer(hidden=ephemeral)
        with open("configs/permissions.json", "r") as file:
            data = json.load(file)
        guildID = str(ctx.guild.id)
        permission = kwargs["permission"]
        user = kwargs["user"]
        value = kwargs["value"]
        userID = str(user.id)
        if value == "true":
            if userID not in data[guildID][permission]:
                data[guildID][permission].append(userID)
        elif userID in data[guildID][permission]:
            data[guildID][permission].remove(userID)
        data[guildID][userID][permission] = value

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
    async def setupPerms(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.defer(hidden=ephemeral)
        with open("configs/permissions.json", "r") as file:
            data = json.load(file)
        guildID = ctx.guild.id
        guild = self.bot.get_guild(guildID)
        guildID = str(guildID)
        try:
            data.pop(guildID)
        except KeyError:
            pass
        data[guildID] = {}
        ids = [member.id for member in guild.members]
        data[guildID]["admin"] = []
        data[guildID]["poggies"] = []
        data[guildID]["lektiescan"] = []
        data[guildID]["banned"] = []
        data[guildID]["bury"] = []
        for memberID in ids:
            data[guildID][memberID] = {
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
    bot.add_cog(Perms(bot))
