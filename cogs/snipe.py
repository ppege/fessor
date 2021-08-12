import discord
from discord.ext import commands
import functions.utils
import datetime

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    snipeMessage = {
    "sender": "none",
    "message": "none",
    "time": "none"
    }

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print("message deleted")
        self.snipeMessage = message

    @functions.utils.banned()
    @commands.command()
    async def snipe(self, ctx):
        embed=discord.Embed(title=f"Sniped!", description=f"Sent at {self.snipeMessage.created_at + datetime.timedelta(hours=2)} by {self.snipeMessage.author.mention}", color=0x00FFFF)
        embed.add_field(name=f"Message content", value=self.snipeMessage.content)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Snipe(bot))
