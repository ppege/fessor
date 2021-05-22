import discord
from discord.ext import commands
import functions.utils

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @commands.command()
    async def kick(self, ctx, member: discord.Member):
      await ctx.guild.kick(member)
      await ctx.send('`%s` kicked - ez' % member)

    @functions.utils.admin()
    @commands.command()
    async def ban(self, ctx, member: discord.Member):
      await ctx.guild.ban(member)
      await ctx.send('`%s` banned - ez' % member)

    @functions.utils.admin()
    @commands.command()
    async def unban(self, ctx, id):
      user = await self.bot.fetch_user(id)
      await ctx.guild.unban(user)
      await ctx.send('`%s` unbanned' % user)

    @functions.utils.admin()
    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" You have been muted. Reason: {reason}")

    @functions.utils.admin()
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
       mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
       await member.remove_roles(mutedRole)
       await member.send(f"Du er unmuted nu NOOB")
       embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been unmuted",colour=discord.Colour.light_gray())
       await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
