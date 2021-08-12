import discord
from discord.ext import commands
import functions.utils
import configparser
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @cog_ext.cog_slash(name="blacklist",
                        description="Add terms to a list, and certain things will happen when said term is spoken.",
                        guild_ids=functions.utils.servers,
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
      config = configparser.ConfigParser()
      config.read('configs/config.ini')
      oldCfg = config['blacklist']['list'].split(', ')
      output = "Error"
      #if len(args) == 0:
        #output = config['blacklist']['list']
        #await ctx.send(embed=discord.Embed(title="Blacklist", description=output))
        #return
      #else:
      if action == "add":
        oldCfg.append(string)
        output = "Successfully added %s to the blacklist!" % (string)
      if action == "remove":
        oldCfg.remove(string)
        output = "Successfully removed %s from the blacklist!" % (string)
      newCfg = ', '.join(oldCfg)
      config['blacklist']['list'] = newCfg
      with open('configs/config.ini', 'w') as configfile:
        config.write(configfile)
      embed=discord.Embed(title=output, description="", color=0xFF0000)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Blacklist(bot))
