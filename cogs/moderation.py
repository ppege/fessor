import discord
from discord.ext import commands
import functions.utils
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @cog_ext.cog_slash(name="kick",
                        description="Kick a user",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="user",
                                description="which user to kick?",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def kick(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.guild.kick(kwargs["user"])
        await ctx.send('`%s` kicked - ez' % kwargs["user"], hidden=ephemeral)

    @functions.utils.admin()
    @cog_ext.cog_slash(name="ban",
                        description="Ban a user",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="user",
                                description="which user to ban?",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def ban(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        user = await self.bot.fetch_user(kwargs["user"])
        await ctx.guild.ban(user)
        await ctx.send('`%s` banned - ez' % user)

    @functions.utils.admin()
    @cog_ext.cog_slash(name="unban",
                        description="Unban a user",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="user",
                                description="which user to unban?",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def unban(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        user = await self.bot.fetch_user(kwargs["user"])
        await ctx.guild.unban(user)
        await ctx.send('`%s` unbanned' % user)

    @functions.utils.admin()
    @cog_ext.cog_slash(name="mute",
                        description="Mute a user",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="user",
                                description="which user to mute?",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="reason",
                                description="reason for muting",
                                option_type=3,
                                required=False
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def mute(self, ctx: discord_slash.SlashContext, **kwargs):
        functions.utils.eCheck(**kwargs)
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        embed = discord.Embed(title="Muted", description=f"{kwargs['user'].mention} was muted", colour=discord.Colour.light_gray())
        embed.add_field(name="Reason:", value=kwargs["reason"], inline=False)
        await ctx.send(embed=embed)
        await kwargs["user"].add_roles(mutedRole, reason=kwargs["reason"])
        await kwargs["user"].send(f" You have been muted. Reason: {kwargs['reason']}")

    @functions.utils.admin()
    @cog_ext.cog_slash(name="unmute",
                        description="Unmute a user",
                        guild_ids=functions.utils.servers,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="user",
                                description="which user to unmute?",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def unmute(self, ctx: discord_slash.SlashContext, **kwargs):
        functions.utils.eCheck(**kwargs)
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await kwargs["user"].remove_roles(mutedRole)
        await kwargs["user"].send(f"Du er unmuted nu NOOB")
        embed = discord.Embed(title="Unmuted", description=f"{kwargs['user'].mention} has been unmuted",colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
