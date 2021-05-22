import discord
from discord.ext import commands
import json
import configparser

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
