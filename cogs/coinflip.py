import discord
from discord.ext import commands
import random
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
import functions.utils

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="coinflip", description="Flips a coin.", guild_ids=functions.utils.servers, default_permission=True, permissions=functions.utils.slPerms("banned"))
    async def coinflip(self, ctx: discord_slash.SlashContext):
        def getResult():
            result = random.uniform(0, 1)
            output = "Heads!" if result > 0.5 else "Tails!"
            return output, result
        output, result = getResult()
        action_row = create_actionrow(create_button(style=ButtonStyle.green, label="Reroll"))

        await ctx.send(embed=discord.Embed(title=output, description=f"Float: {str(result)}", color=0xFF0000), components=[action_row])

        while(True):
            button_ctx: discord_slash.ComponentContext = await wait_for_component(self.bot, components=action_row)
            output, result = getResult()
            await button_ctx.edit_origin(embed=discord.Embed(title=output, description=f"Float: {str(result)}", color=0xFF0000))

def setup(bot):
    bot.add_cog(Coinflip(bot))
