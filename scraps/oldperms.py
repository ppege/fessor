import discord
from discord.ext import commands
import functions.utils
import configparser
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class Perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.admin()
    @cog_ext.cog_slash(name="perms",
                        description="Manage permissions",
                        guild_ids=[811552770074738688],
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
    async def perms(self, ctx, *args):
      def idHandler(id):
        if "<@!" in id:
          id = id.replace('<@!', '').replace('>', '')
        elif "<@" in id:
          id = id.replace('<@', '').replace('>', '')
        else:
          id = id
        return id
      if args[0] == 'reset':
        ids = [member.id for member in ctx.guild.members]
        print(str(ids))
        for i in range(0, len(ids)):
          config = configparser.ConfigParser()
          config.read('configs/config.ini')
          config[str(ids[i])] = {'admin': 'false', 'settings': 'false', 'poggies': 'true', 'lektiescan': 'true', 'banned': 'false', 'slander': 'true', 'bury': 'true'}
          with open('configs/config.ini', 'w') as configfile:
            config.write(configfile)
        output = "permissions have been reset"
        embed=discord.Embed(title=output, description="", color=0xFF0000)
        await ctx.send(embed=embed)
      elif len(args) == 1 and "<@" in args[0]:
        id = idHandler(args[0])
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        userConfig = config[id]
        userName = self.bot.get_user(int(id)).name
        outputTitle = userName + "'s permissions"
        output = "`Admin: %s\nSettings: %s\nPoggies: %s\nLektiescan: %s\nBanned: %s\nSlander: %s`" % (userConfig['admin'], userConfig['settings'], userConfig['poggies'], userConfig['lektiescan'], userConfig['banned'], userConfig['slander'])
        embed=discord.Embed(title=outputTitle, description=output, color=0xFF0000)
        await ctx.send(embed=embed)
      else:
        id = idHandler(args[0])
        permission = args[1]
        value = args[2]
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        config[id][permission] = value
        with open('configs/config.ini', 'w') as configfile:
          config.write(configfile)
        output = id + "'s '" + permission + "' permission has been set to '" + value + "'"
        embed=discord.Embed(title=output, description="", color=0xFF0000)
        await ctx.send(embed=embed)

def setup(bot):
    #bot.add_cog(Perms(bot))
    print("hi")
