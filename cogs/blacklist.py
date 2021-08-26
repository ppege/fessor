"""This cog adds the blacklist command, which lets admins block strings from chat"""
# pylint: disable=unspecified-encoding
import configparser
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import functions.utils # pylint: disable=import-error

class Blacklist(commands.Cog):
    """Blacklist cog"""
    def __init__(self, bot):
        """Loads the cog"""
        self.bot = bot

    @cog_ext.cog_slash(name="blacklist",
                        description="Add terms to a list to block them.",
                        guild_ids=functions.utils.servers,
                        default_permission=False,
                        permissions=functions.utils.slPerms("admin"),
                        options=[
                            create_option(
                                name="action",
                                description="to add or to remove, that is the question",
                                option_type=3,
                                required=True,
                                choices=[
                                    create_choice(
                                        name="add",
                                        value="add"
                                    ),
                                    create_choice(
                                        name="remove",
                                        value="remove"
                                    )
                                ]
                            ),
                            create_option(
                                name="string",
                                description="the string that will be caught",
                                option_type=3,
                                required=True
                            )
                        ]
    )

    async def blacklist(self, ctx: discord_slash.SlashContext, action, string):
        """The blacklist command"""
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        old_cfg = config['blacklist']['list'].split(', ')
        output = "Error"
        if action == "add":
            old_cfg.append(string)
            output = "Successfully added %s to the blacklist!" % (string)
        if action == "remove":
            old_cfg.remove(string)
            output = "Successfully removed %s from the blacklist!" % (string)
        new_cfg = ', '.join(old_cfg)
        config['blacklist']['list'] = new_cfg
        with open('configs/config.ini', 'w') as configfile:
            config.write(configfile)
        embed=discord.Embed(title=output, description="", color=0xFF0000)
        await ctx.send(embed=embed)

def setup(bot):
    """Adds the cog"""
    bot.add_cog(Blacklist(bot))
