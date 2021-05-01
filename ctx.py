from discord.ext import commands
from discord.utils import get
import os
import discord
import discord.ext.commands
import asyncio
from functions.school import schedule
import datetime
import os,sys,inspect
from functions.fun.slander import slander
from configs import options
import configparser
from functions.school.lektiescanner import lektiescan
from threading import Timer
import pytz
import time
from keep_alive import keep_alive
startTime = time.time()
def getUptime():
    uptime = time.time() - startTime
    return str(datetime.timedelta(seconds=uptime))

if os.getenv('mode') == "updates":
  prefix = ','
else:
  prefix = '.'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

async def notify(id, cause):
  if cause == 'banned':
    output = 'Fucking mongol, du er BANNET fra FESSOR BOT :joy:'
  elif cause == 'no':
    output = 'Du har ikke tilladelse til denne kommando IDIOT'
  elif cause == 'locked':
    output = 'Botten er låst lige nu LEL'
  else:
    output = 'Jeg ved ikke hvorfor du får denne besked, sig det til william pls'
  user = bot.get_user(id)
  await user.send(output)

async def check(id, permission):
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  allowed = "no"
  id = str(id)
  if config[id][permission] == 'true':
    allowed = "yes"
  if config[id]['banned'] == 'true':
    allowed = "banned"
  if config['config']['lock'] == 'on':
    allowed = "locked"
  if config[id]['admin'] == 'true':
    allowed = "yes"
  if allowed != "yes":
    await notify(int(id), allowed)
  return allowed

def idHandler(id):
  if "<@!" in id:
    id = id.replace('<@!', '').replace('>', '')
  elif "<@" in id:
    id = id.replace('<@', '').replace('>', '')
  else:
    id = id
  return id


@bot.event
async def on_ready():
  print('CTX READY.')
  print('{0.user}'.format(bot))
  await bot.change_presence(activity=discord.Game(name="matematikfessor.dk"))

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  if any(word in message.content.lower() for word in config['blacklist']['list'].split(', ')):
    try:
      await message.delete()
    except:
      await message.add_reaction('🇱')
  if message.author.id == 159985870458322944:
    await message.channel.send('Luk røven MEE6')
  if message.content == ".shutdown" and config[str(message.author.id)]['admin'] == "true":
    sys.exit()
  if message.content == "pingmain":
    print('main pinged')
    await message.channel.send('pongmain')

@bot.command()
async def status(ctx):
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  uptime = getUptime()
  description = f"Uptime: `{uptime}`\nMode: `{os.getenv('mode')}`\nVersion: `{config['config']['version']}`"
  embed=discord.Embed(title='Status', description=description, color=0x000143)
  embed.set_footer(text='Created and maintained by Nangu')
  await ctx.send(embed=embed)

@bot.command()
async def ping(ctx, *args):
  print('ctx pinged')
  if len(args) == 0:
    await ctx.send('pong!')
  else:
    await ctx.send(" ".join(args))

@bot.command()
async def s(ctx, victim):
  allowed = await check(ctx.author.id, 'slander')
  if allowed != "yes": return
  try:
    output = slander[victim]
    await ctx.send(output)
  except:
    embed=discord.Embed(title="Slander fejl", description="Dette slander findes ikke\nListe af slander:\n`william`\n`noah`\n`jeppe`\n`mads`\n`jakob`\n`peter`\n`asger`\n`frederik`\n`emil`\n`simon`", color=0xFF0000)
    await ctx.send(embed=embed)

@bot.command()
async def suggest(ctx, suggestion):
  f = open("suggestions.md", "a")
  content = "\n## Suggestion from %s\n- %s" % (ctx.author, suggestion)
  f.write(content)
  f.close
  user = bot.get_user(273845229130481665)
  await user.send(embed=discord.Embed(title='Suggestion from %s' % ctx.author, description=suggestion, color=0xFF0000))
  await ctx.send(embed=discord.Embed(title='Suggestion sendt', description=suggestion, color=0xFF0000))

@bot.command()
async def skema(ctx, *args):
  if len(args) == 0:
    today = datetime.datetime.today().weekday()
    if today >= 5:
      await ctx.send('Det er ikke en ugedag, antager mandag.')
      today = 0
    today = str(today)
    output = options.schedules[today]
    await ctx.send(output)
  else:
    try:
      await ctx.send(options.skemaer[args[0]])
    except:
      await ctx.send('Invalid dag, mongol')

#@bot.command()
async def overview(ctx, *args):
  if len(args) == 0:
    await ctx.send('I dag, i morgen eller en dato?')
    userInput = await bot.wait_for("message")
    if userInput.content.lower() == "i dag":
      now = datetime.datetime.now()
      hours = 2
      hours_added = datetime.timedelta(hours = hours)
      newtime = now + hours_added
      fulltime = newtime.strftime('%d. %b %H:%M').replace('Oct', 'Okt').lower()
      currentDate =  newtime.strftime('%d. %b').replace('Oct', 'Okt').lower()
      dato=currentDate
    elif userInput.content.lower() == "i morgen":
      now = datetime.datetime.now()
      hours = 2
      hours_added = datetime.timedelta(hours = hours)
      newtime = now + hours_added
      days = 1
      days_added = datetime.timedelta(days = days)
      newnewtime = newtime + days_added
      fulltime = newnewtime.strftime('%d. %b %H:%M').replace('Oct', 'Okt').lower()
      currentDate =  newnewtime.strftime('%d. %b').replace('Oct', 'Okt').lower()
      await ctx.send(currentDate)
      dato=currentDate
    else:
      dato=userInput
  else:
    dato=' '.join(args)
    print(dato)

  status = await ctx.send(embed=discord.Embed(title="Scanner viggo...", description=""))
  begivenhed, beskrivelse, author, files, tidspunkt, fileNames = lektiescan(ctx)
  numList = []
  for i in range(0, len(tidspunkt)):
    if dato in tidspunkt[i]:
      numList.append(i)
  userInput = numList
  print(str(userInput))
  async def lektier():
    response = await post(ctx, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, userInput)
    await status.delete()
    if response == "fail":
      await status.edit(embed=discord.Embed(title="Ingen lektier fundet", description="", color=0xFF0000))
  def skema():
    print('nothign')

@bot.command()
async def modify(ctx, category, key, value):
  allowed = await check(ctx.author.id, 'admin')
  if allowed != "yes": return
  config = configparser.ConfigParser()
  config.read('configs/assets.ini')
  config[category][key] = value
  with open('configs/assets.ini', 'w') as configfile:
    config.write(configfile)
  output = "Successfully replaced"
  embed=discord.Embed(title=output, description="", color=0xFF0000)
  await ctx.send(embed=embed)

@bot.command()
async def scan(ctx, *args):
    try:
      if len(args) == 0:
        argsPresent = False
      else:
        argsPresent = True
        userInput = ' '.join(args)

      status = await ctx.send(embed=discord.Embed(title="Scanner viggo...", description=""))
      begivenhed, beskrivelse, author, files, tidspunkt, fileNames, url = lektiescan(ctx)
      if argsPresent == False:
        lektieList = []
        for i in range(0, len(begivenhed)):
          lektieList.append(str(i + 1) + ". " + begivenhed[i] + " | Afleveres " + tidspunkt[i])
        description = "\n\n".join(lektieList)
        Field2 = "Mulighed 1. Skriv tallet, der tilhænger den lektie, du vil se.\nMulighed 2. Skriv `søg [fag]`.\nMulighed 3. Skriv `dato [dato]`."
        embed=discord.Embed(title="Fandt %d lektier" % len(begivenhed), description=description, color=0xFF0000)
        embed.add_field(name="Hvad nu?", value=Field2)
        await status.edit(embed=embed)
        userInput = await bot.wait_for("message")
        userInput = userInput.content
      else:
        await status.delete()
      isInt = 0
      try:
        int(userInput)
        userInput = int(userInput)
        isInt = 1
      except:
        isInt = 0
      if isInt == 1:
        userInput = [userInput - 1]
      else:
        splitInput = userInput.split(' ')
        if splitInput[0] == "søg":
          userInput = userInput.replace('søg ', '')
          numList = []
          for i in range(0, len(begivenhed)):
            if str(userInput) in begivenhed[i]:
              numList.append(i)
          userInput = numList
        elif splitInput[0] == "dato":
          userInput = userInput.replace('dato ', '')
          numList = []
          for i in range(0, len(begivenhed)):
            if str(userInput) in tidspunkt[i]:
              numList.append(i)
          userInput = numList
      print(str(userInput))
      try:
        await post(ctx, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, userInput, url)
      except:
        await ctx.send(embed=discord.Embed(title="EPIC FAIL :rofl:", description="Du skal skrive et tal, der passer til de lektier, botten har fundet!!!!! :rage::rage::rage:"))
        raise
    except:
      raise
      await ctx.send(embed=discord.Embed(title="Scan fejlede.", description="", color=0xFF0000))

@bot.command()
async def settings(ctx, setting, value):
  allowed = await check(ctx.author.id, 'settings')
  if allowed != "yes": return
  try:
    if setting not in options.settings or value not in options.values:
      embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
      embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
      await ctx.send(embed=embed)
    else:
      config = configparser.ConfigParser()
      config.read('configs/config.ini')
      config['config'][setting] = value
      with open('configs/config.ini', 'w') as configfile:
        config.write(configfile)
      output = setting + "has been set to " + value
      embed=discord.Embed(title=output, description="", color=0xFF0000)
  except:
    embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
    embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def shutdown(ctx):
  allowed = await check(ctx.author.id, 'admin')
  if allowed != "yes": return
  await ctx.send(embed=discord.Embed(title='Shutting down...', description='', color=0x0000FF))
  os.system('python3 fallback.py &')
  sys.exit(0)

@bot.command()
async def bury(ctx):
  allowed = await check(ctx.author.id, 'bury')
  if allowed != "yes": return
  for i in range(0, 5):
    await ctx.send('https://i.imgur.com/SL9KqwC.png')

@bot.command()
async def blacklist(ctx, *args):
  config = configparser.ConfigParser()
  config.read('configs/config.ini')
  oldCfg = config['blacklist']['list'].split(', ')
  output = "Error"
  if len(args) == 0:
    output = config['blacklist']['list']
    await ctx.send(embed=discord.Embed(title="Blacklist", description=output))
    return
  else:
    if args[0] == "add":
      oldCfg.append(args[1])
      output = "Successfully added %s to the blacklist!" % (args[1])
    if args[0] == "remove":
      oldCfg.remove(args[1])
      output = "Successfully removed %s from the blacklist!" % (args[1])
  newCfg = ', '.join(oldCfg)
  config['blacklist']['list'] = newCfg
  with open('configs/config.ini', 'w') as configfile:
    config.write(configfile)
  embed=discord.Embed(title=output, description="", color=0xFF0000)
  await ctx.send(embed=embed)
    

@bot.command()
async def poggies(ctx):
  allowed = await check(ctx.author.id, 'poggies')
  if allowed != "yes": return
  f = open("poggers.txt", "r")
  fileContent = f.read()
  output = fileContent.split('\n')
  for i in range(0, len(output)):
    await ctx.send(output[i])

@bot.command()
async def badass(ctx):
  await ctx.send('https://imgur.com/a/QqFEkrm')

@bot.command()
async def perms(ctx, *args):
  allowed = await check(ctx.author.id, 'admin')
  if allowed != "yes": return
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
    userName = bot.get_user(int(id)).name
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

@bot.command()
async def next(ctx):
    today = datetime.datetime.today().weekday()
    today = str(today)
    usedSchedule = "L"
    if today == "0":
      usedSchedule = schedule.monday
    elif today == "1":
      usedSchedule = schedule.tuesday
    elif today == "2":
      usedSchedule = schedule.wednesday
    elif today == "3":
      usedSchedule = schedule.thursday
    elif today == "4":
      usedSchedule = schedule.friday
    now = datetime.datetime.now()
    hours = 2
    hours_added = datetime.timedelta(hours = hours)
    newtime = now + hours_added
    currentTime = newtime.strftime("%H:%M")
    print(currentTime)
    currentTime = int(str(currentTime).replace(':', ''))
    nextClass = "There is no next class today."
    classNum = 0
    for i in range(0, 7):
      if currentTime > schedule.times[i]:
        classNum = i
      else:
        classNum = classNum
    try:
      nextClass = schedule.times[classNum + 1]
    except:
      nextClass = "Der er ingen timer din klovn"
    await ctx.send(nextClass)

@bot.command()
async def halp(ctx, *args):
  print('1')
  commandList = list(options.commands.keys())
  newCommandList = "\n".join(commandList)
  if len(args) == 0:
    embed = discord.Embed(title='Kommandoliste', description=newCommandList)
    embed.add_field(name='Brug `.halp [kommando]` for mere info', value='lel')
    await ctx.send(embed=embed)
  else:
    title = args[0]
    description = options.commands[args[0]]
    embed = discord.Embed(title=title, description=description)
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member):
  await ctx.guild.kick(member)
  await ctx.send('`%s` kicked - ez' % member)

@bot.command()
async def ban(ctx, member: discord.Member):
  await ctx.guild.ban(member)
  await ctx.send('`%s` banned - ez' % member)

@bot.command()
async def unban(ctx, id):
  user = await bot.fetch_user(id)
  await ctx.guild.unban(user)
  await ctx.send('`%s` unbanned' % user)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
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

@bot.command()
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.remove_roles(mutedRole)
   await member.send(f"Du er unmuted nu NOOB")
   embed = discord.Embed(title="Unmuted", description=f"{member.mention} has been unmuted",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

async def post(ctx, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, selection, url):
  print('post() called')
  try:
    print(selection[0])
  except:
    print('poop')
    return "fail"
  if selection[0] == -1:
    for i in range(0, len(begivenhed)):
      #print('creating post %d' % i)
      currentClass = begivenhed[i]
      currentTeacher = author[i]
      embedColor = 0xFF5733
      #print('registering colors')
      if currentClass == 'Tysk' or currentClass == 'Kristendom':
        embedColor = 0x9900FF
      elif currentClass == 'Dansk eller fysik' or currentClass ==  'Dansk':
        embedColor = 0xFF0000
      elif currentClass == 'Engelsk' or currentClass == 'Matematik':
        embedColor = 0x0000FF
      elif currentClass == 'Billedkunst':
        embedColor = 0xFFFF00
      elif currentClass == 'Geografi' or currentClass == 'Biologi':
        embedColor = 0x00FF00
      elif currentClass == 'Historie' or currentClass == 'Samfundsfag':
        embedColor = 0xFF9900
      elif currentClass == 'Idræt':
        embedColor = 0x00FFFF
      #print('colors registered')
      if 1 == 1:
          #print('registering thumbnails')
          embedThumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"
          if "Birte Holst Andersen" in currentTeacher:
            embedThumbnail = "https://www.meaningfulwomen.com/wp-content/uploads/grumpy-old-woman.jpg"
          elif "Anne-Mette Hessel" in currentTeacher:
            embedThumbnail = "https://www.hjv.dk/oe/HDNJY/nyheder/PublishingImages/Anne-Mette%20Hessel%20p%C3%A5%20trombone.jpg"
          elif "Camilla Willemoes Holst" in currentTeacher:
            embedThumbnail = "https://legacy.tyt.com/wp-content/uploads/Crazy-Lady-Casually-Stabs-Innocent-People-on-The-Street-Disturbing-Video.jpg"
          elif "Jens Pedersen" in currentTeacher:
            embedThumbnail = "https://images.halloweencostumes.com/products/9073/1-1/wild-caveman-costume.jpg"
          elif "Stig Andersen" in currentTeacher:
            embedThumbnail = "https://upload.wikimedia.org/wikipedia/commons/7/7c/Cima_da_Conegliano%2C_God_the_Father.jpg"
          elif "Jacob Albrechtsen" in currentTeacher:
            embedThumbnail = "assets/viggo/teachers/jacob.jpg"
          elif "Anne Isaksen Østergaard" in currentTeacher:
            embedThumbnail = "https://cdn.store-factory.com/www.couteaux-services.com/content/product_9732713b.jpg?v=1518691523"
          #print('thumbnails registered, handling files')
          forLoopFiles = []
          for j in range(0, len(files[i].split(','))):
            forLoopFiles.append(files[i].split(',')[j])
          forLoopFileNames = []
          for j in range(0, len(fileNames[i].split(','))):
            forLoopFileNames.append(fileNames[i].split(',')[j])
          fileOutput = ""
          for k in range(0, len(forLoopFiles)):
            fileOutput = fileOutput + "[" + forLoopFileNames[k] + "](" + forLoopFiles[k] + ")\n"
          #print('files handled, creating embed')
          embed=discord.Embed(title=begivenhed[i], description=tidspunkt[i], color=embedColor, url=url[i])
          embed.add_field(name="Beskrivelse", value=beskrivelse[i], inline=True)
          embed.set_footer(text=f"{author[i]}")
          embed.add_field(name="Filer", value=fileOutput, inline=True)
          embed.set_thumbnail(url=embedThumbnail)
          print('embed %d created, sending embed' % i)
          await ctx.send(embed=embed)
          #print('embed sent, reiterating for loop or returning')
  else:
    for i in range(0, len(selection)):
      #print('creating post %d' % i)
      currentClass = begivenhed[selection[i]]
      currentTeacher = author[selection[i]]
      embedColor = 0xFF5733
      #print('registering colors')
      if currentClass == 'Tysk' or currentClass == 'Kristendom':
        embedColor = 0x9900FF
      elif currentClass == 'Dansk eller fysik' or currentClass ==  'Dansk':
        embedColor = 0xFF0000
      elif currentClass == 'Engelsk' or currentClass == 'Matematik':
        embedColor = 0x0000FF
      elif currentClass == 'Billedkunst':
        embedColor = 0xFFFF00
      elif currentClass == 'Geografi' or currentClass == 'Biologi':
        embedColor = 0x00FF00
      elif currentClass == 'Historie' or currentClass == 'Samfundsfag':
        embedColor = 0xFF9900
      elif currentClass == 'Idræt':
        embedColor = 0x00FFFF
      #print('colors registered')
      if 1 == 1:
          #print('registering thumbnails')
          assets = configparser.ConfigParser()
          assets.read('configs/assets.ini')
          embedThumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"
          if "Birte Holst Andersen" in currentTeacher:
            embedThumbnail = "birte"
          elif "Anne-Mette Hessel" in currentTeacher:
            embedThumbnail = "annemette"
          elif "Camilla Willemoes Holst" in currentTeacher:
            embedThumbnail = "camilla"
          elif "Jens Pedersen" in currentTeacher:
            embedThumbnail = "jens"
          elif "Stig Andersen" in currentTeacher:
            embedThumbnail = "stig"
          elif "Jacob Albrechtsen" in currentTeacher:
            embedThumbnail = "jacob"
          elif "Anne Isaksen Østergaard" in currentTeacher:
            embedThumbnail = "anne"
          if "https" not in embedThumbnail:
            embedThumbnail = assets['teachers'][embedThumbnail]
          #print('thumbnails registered, handling files')
          forLoopFiles = []
          for j in range(0, len(files[selection[i]].split(','))):
            forLoopFiles.append(files[selection[i]].split(',')[j])
          forLoopFileNames = []
          for j in range(0, len(fileNames[selection[i]].split(','))):
            forLoopFileNames.append(fileNames[selection[i]].split(',')[j])
          fileOutput = ""
          for k in range(0, len(forLoopFiles)):
            fileOutput = fileOutput + "[" + forLoopFileNames[k] + "](" + forLoopFiles[k] + ")\n"
          #print('files handled, creating embed')
          embed=discord.Embed(title=begivenhed[selection[i]], description=tidspunkt[selection[i]], color=embedColor, url=url[selection[i]])
          embed.add_field(name="Beskrivelse", value=beskrivelse[selection[i]], inline=True)
          embed.set_footer(text=f"{author[selection[i]]}")
          embed.add_field(name="Filer", value=fileOutput, inline=True)
          embed.set_thumbnail(url=embedThumbnail)
          print('embed %d created, sending embed' % selection[i])
          await ctx.send(embed=embed)
          #print('embed sent, reiterating for loop or returning')
  return "success"

keep_alive()
bot.run(os.getenv('fessortoken'))
