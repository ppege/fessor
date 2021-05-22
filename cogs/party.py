import discord
from discord.ext import commands
import functions.utils
import json
import string

class Party(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def party(self, ctx, *args):
      if args[0] == "create":
        id = ''.join((random.choice(string.ascii_letters) for x in range(4)))
        file = open("configs/parties.json", "r")
        config = json.load(file)
        file.close()
        guild = ctx.guild
        member = ctx.author
        accessRole = await guild.create_role(name=id)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),
            guild.me: discord.PermissionOverwrite(connect=True),
            accessRole: discord.PermissionOverwrite(connect=True)
        }
        channel = await guild.create_voice_channel(f"{member}'s party", overwrites=overwrites)
        await ctx.author.add_roles(accessRole)
        config["dict"][id] = {
          "owner": member.id,
          "role": accessRole.id,
          "channel": channel.id,
          "members": {}
        }
        file = open("configs/parties.json", "w")
        json.dump(config, file)
        file.close()
        embed=discord.Embed(title="Party created", description=f"The ID of your party is {id}", color=0xFF0000)
        await ctx.send(embed=embed)
      elif args[0] == "add":
        member = int(idHandler(args[1]))
        file = open("configs/parties.json", "r")
        config = json.load(file)
        file.close()
        guild = ctx.guild
        member = guild.get_member(member)
        id = args[2]
        if ctx.author.id != config["dict"][id]["owner"]:
          await ctx.send(embed=discord.Embed(title="You aren't the owner of this party!", description="The owner of the party is <@" + str(config["dict"][id]["owner"]) + ">."))
          return
        accessRole = discord.utils.get(guild.roles, name=args[2])
        roleId = config["dict"][id]["role"]
        await member.add_roles(guild.get_role(roleId))
        config["dict"][id]["members"][member.id] = member.name
        file = open("configs/parties.json", "w")
        json.dump(config, file)
        file.close()
        embed=discord.Embed(title="Member added", description=f"<@{member.id}> was added to the party.", color=0xFF0000)
        await ctx.send(embed=embed)
      elif args[0] == "remove":
        member = int(idHandler(args[1]))
        file = open("configs/parties.json", "r")
        config = json.load(file)
        file.close()
        guild = ctx.guild
        member = guild.get_member(member)
        id = args[2]
        if ctx.author.id != config["dict"][id]["owner"]:
          await ctx.send(embed=discord.Embed(title="You aren't the owner of this party!", description="The owner of the party is <@" + str(config["dict"][id]["owner"]) + ">."))
          return
        accessRole = discord.utils.get(guild.roles, name=args[2])
        roleId = config["dict"][id]["role"]
        await member.remove_roles(guild.get_role(roleId))
        del config["dict"][id]["members"][str(member.id)]
        file = open("configs/parties.json", "w")
        json.dump(config, file)
        file.close()
        embed=discord.Embed(title="Member removed", description=f"<@{member.id}> was removed from the party.", color=0xFF0000)
        await ctx.send(embed=embed)
      elif args[0] == "disband":
        file = open("configs/parties.json", "r")
        config = json.load(file)
        file.close()
        guild = ctx.guild
        id = args[1]
        if ctx.author.id != config["dict"][id]["owner"]:
          await ctx.send(embed=discord.Embed(title="You aren't the owner of this party!", description="The owner of the party is <@" + str(config["dict"][id]["owner"]) + ">."))
          return
        roleId = config["dict"][id]["role"]
        role = guild.get_role(roleId)
        await role.delete()
        channelId = config["dict"][id]["channel"]
        channel = guild.get_channel(channelId)
        await channel.delete()
        del config["dict"][id]
        file = open("configs/parties.json", "w")
        json.dump(config, file)
        file.close()
        embed=discord.Embed(title="Party disbanded.", description="", color=0xFF0000)
        await ctx.send(embed=embed)
      elif args[0] == "list":
        file = open("configs/parties.json", "r")
        config = json.load(file)
        file.close()
        keys = config["dict"].keys()
        keys = list(keys)
        embed=discord.Embed(title="Party list", description="List of all parties", color=0x00FFFF)
        names = []
        values = []
        for i in range(len(keys)):
          print(i)
          names.append(keys[i])
          try:
            keys2 = config["dict"][keys[i]]["members"].keys()
            keys2 = list(keys2)
            members = ""
            for j in range(len(keys2)):
              members = members + f"\n<@{keys2[j]}>"
            values.append(f'Owner: <@{config["dict"][keys[i]]["owner"]}>\n Members: {members}')
          except:
            values.append(f'Owner: <@{config["dict"][keys[i]]["owner"]}>\n No members')
          embed.add_field(name=names[i], value=values[i])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Party(bot))
