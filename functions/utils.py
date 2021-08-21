import discord
from discord.ext import commands
import json
import configparser
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType

config = configparser.ConfigParser()
config.read('cred.ini')

if config['config']['mode'] == "updates":
    servers = [
        878614900824485900
    ]
else:
    servers = [
        799253855677579285,
        811552770074738688
    ]

def slPerms(permission):
    with open("configs/permissions.json", "r") as file:
        data = json.load(file)
    if config['config']['mode'] == "main":
        if permission == "dev":
            permissions={
                811552770074738688: [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ],
                799253855677579285: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
        elif permission == "banned":
            permissions={
                811552770074738688: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["811552770074738688"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ],
                799253855677579285: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["799253855677579285"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
        else:
            permissions={
                811552770074738688: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["811552770074738688"][permission]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["811552770074738688"]["admin"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["811552770074738688"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ],
                799253855677579285: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["799253855677579285"][permission]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["799253855677579285"]["admin"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["799253855677579285"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
    else:
        if permission == "dev":
            permissions={
                878614900824485900: [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
        elif permission == "banned":
            permissions={
                878614900824485900: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["878614900824485900"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
        else:
            permissions={
                878614900824485900: 
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["878614900824485900"][permission]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["878614900824485900"]["admin"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, False) for userID in data["878614900824485900"]["banned"]
                ] +
                [
                    create_permission(int(userID), SlashCommandPermissionType.USER, True) for userID in data["developers"]
                ]
            }
    return permissions

def idHandler(id):
  if "<@!" in id:
    id = id.replace('<@!', '').replace('>', '')
  elif "<@" in id:
    id = id.replace('<@', '').replace('>', '')
  else:
    id = id
  return id

def admin():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['admin'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def settings():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['settings'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        if config[str(ctx.author.id)]['admin'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def poggies():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['poggies'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        if config[str(ctx.author.id)]['admin'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def lektiescan():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['lektiescan'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        if config[str(ctx.author.id)]['admin'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def banned():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def slander():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['slander'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        if config[str(ctx.author.id)]['admin'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def bury():
    def wrapper(ctx):
        config = configparser.ConfigParser()
        config.read('configs/config.ini')
        if config[str(ctx.author.id)]['bury'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        if config[str(ctx.author.id)]['admin'] == 'true' and config[str(ctx.author.id)]['banned'] == 'false':
            return True
        return False
    return commands.check(wrapper)

def eCheck(**kwargs):
    try:
        print(kwargs["private"])
    except:
        return False
    if kwargs["private"] == True:
        return True
    else:
        return False
