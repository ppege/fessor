import discord
import os
import schedule
import datetime
from threading import Timer
import pytz
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
import asyncio
import file
import lektiescanner

def scan():
  import lektiescanner

client = discord.Client()
bot = commands.Bot(command_prefix='.')

funnymode = False

def split(word): 
    return [char for char in word] 

scan()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="Viggo destruction simulator 2021"))
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  f = open("config.py", "r")
  config = f.read()
  f.close()
  if message.author.id != 273845229130481665 and "lock = \"on\"" in config:
    return
  if message.content.startswith('.settings'):
    print('settings registrered')
    input = message.content.split(' ')
    print(str(input))
    print(len(input))
    if len(input) == 1:
      print('entered the help section')
      embed=discord.Embed(title="Settings", description="Prefix til alle settings er \".settings\"\nF.eks. \".settings funnymode on\"", color=0xFF0000)
      embed.add_field(name="Settings", value="**lock**/**unlock**: gør så kun NAANGU kan bruge botten :sunglasses:\n**funnymode on**/**off**: tænder/slukker funny mode, har ingen brug endnu\n**shutdown**: nødssituations shutdown, kun NAAANGUUU kan bruge den lige meget hvad", inline=True)
      await message.channel.send(embed=embed)
    else:
      if input[1] == 'lock' and message.author.id == 273845229130481665:
        f = open("config.py", "r")
        oldConfig = f.read()
        f.close()
        newConfig = oldConfig.replace('lock = "off"', 'lock = "on"')
        f = open("config.py", "w")
        f.write(newConfig)
        f.close()
        embed=discord.Embed(title="Locked", description="#rekt", color=0xFF0000)
        await message.channel.send(embed=embed)
      elif input[1] == 'unlock' and message.author.id == 273845229130481665:
        f = open("config.py", "r")
        oldConfig = f.read()
        f.close()
        newConfig = oldConfig.replace('lock = "on"', 'lock = "off"')
        f = open("config.py", "w")
        f.write(newConfig)
        f.close()
        embed=discord.Embed(title="Unlocked", description="#unrekt", color=0xFF0000)
        await message.channel.send(embed=embed)
  if message.content == '.poggers' or if message.content == '.poggies':
    f = open("poggers.txt", "r")
    output = f.read()
    f.close()
    await message.channel.send(output)
  if message.content == '.badass':
    await message.channel.send('https://imgur.com/a/QqFEkrm')
  if message.content == '.jakob':
    await message.channel.send('https://media.discordapp.net/attachments/803960364907626499/805823820421398578/unknown.png?width=1217&height=676')
  if message.content.startswith('.funnymode'):
    input = message.content.replace('.funnymode ', '')
    if input == 'on':
      funnymode = True
      await message.channel.send('Funnymode is now on')
    elif input == 'off':
      funnymode = False
      await message.channel.send('Funnymode is now off')
    else:
      await message.channel.send('Correct syntax is \'.funnymode on\' or \'.funnymode off\', you moronic idiot.')
  if message.content == '.chris':
    await message.channel.send('https://pbs.twimg.com/profile_images/508735114134581248/JIBaXzgh.png')
  if message.content == 'printall':
    #lektiescanner.begivenhed.clear()
    #lektiescanner.author.clear()
    #lektiescanner.tidspunkt.clear()
    #lektiescanner.files.clear()
    #lektiescanner.fileNames.clear()
    #lektiescanner.beskrivelse.clear()
    #print(str(lektiescanner.begivenhed) + str(lektiescanner.author) + str(lektiescanner.tidspunkt) + str(lektiescanner.files) + str(lektiescanner.fileNames) + str(lektiescanner.beskrivelse))
    #print(str(lektiescanner.begivenhed) + str(lektiescanner.author) + str(lektiescanner.tidspunkt) + str(lektiescanner.files) + str(lektiescanner.fileNames) + str(lektiescanner.beskrivelse))
    print('pre-scan: ' + str(lektiescanner.begivenhed))
    scan()
    print('post-scan: ' + str(lektiescanner.begivenhed))
    for i in range(0, len(lektiescanner.begivenhed)):
      currentClass = lektiescanner.begivenhed[i]
      currentTeacher = lektiescanner.author[i]
      embedColor = 0xFF5733
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
      if 1 == 1:
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
          embedThumbnail = "https://babyinstituttet.dk/wp-content/uploads/2018/09/sund-og-rask-baby.jpg"
        elif "Anne Isaksen Østergaard" in currentTeacher:
          embedThumbnail = "https://cdn.store-factory.com/www.couteaux-services.com/content/product_9732713b.jpg?v=1518691523"
      forLoopFiles = []
      for j in range(0, len(lektiescanner.files[i].split(','))):
        forLoopFiles.append(lektiescanner.files[i].split(',')[j])
      forLoopFileNames = []
      for j in range(0, len(lektiescanner.fileNames[i].split(','))):
        forLoopFileNames.append(lektiescanner.fileNames[i].split(',')[j])
      fileOutput = ""
      for k in range(0, len(forLoopFiles)):
        fileOutput = fileOutput + "[" + forLoopFileNames[k] + "](" + forLoopFiles[k] + ")\n"
      embed=discord.Embed(title=lektiescanner.begivenhed[i], description=lektiescanner.tidspunkt[i], color=embedColor)
      embed.add_field(name="Beskrivelse", value=lektiescanner.beskrivelse[i], inline=True)
      embed.set_footer(text=lektiescanner.author[i])
      embed.add_field(name="Filer", value=fileOutput, inline=True)
      embed.set_thumbnail(url=embedThumbnail)
      await message.channel.send(embed=embed)
  if message.content == 'printone':
    embed=discord.Embed(title=lektiescanner.begivenhed[0], description=lektiescanner.tidspunkt[0], color=0xFF5733)
    embed.add_field(name="Beskrivelse", value=lektiescanner.beskrivelse[0], inline=True)
    embed.set_footer(text=lektiescanner.author[0])
    embed.add_field(name="Filer", value="[" + lektiescanner.fileNames[0] + "](" + lektiescanner.files[0] + ")", inline=True)
    #embed.add_field(name="PLACEHOLDER", value="PLACEHOLDER", inline=True)
    await message.channel.send(embed=embed)
    await message.channel.send(lektiescanner.fileNames[0])
  if message.content == 'tak, fessor':
    await message.channel.send('Intet problem')
  if message.content == '.noah':
    await message.channel.send('https://tenor.com/view/stpattysday-st-patricks-day-irish-gif-5216374')
  if message.content == '.mads':
    await message.channel.send('https://upload.wikimedia.org/wikipedia/commons/8/80/Farmer%2C_Nicaragua.jpg')
  if message.content.startswith('.asger'):
    await message.channel.send("https://i.pinimg.com/originals/0a/e3/bb/0ae3bb9a212d8ec7925b4672b6557582.jpg")
  if message.content.startswith('-next'):
    today = datetime.datetime.today().weekday()
    today = str(today)
    usedSchedule = "Stupid ass idiot"
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
    hours = 1
    hours_added = datetime.timedelta(hours = hours)
    newtime = now + hours_added
    currentTime = newtime.strftime("%H:%M")
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
    await message.channel.send(nextClass)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason='Fuck you retard'):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')

@bot.command()
async def addrole(ctx, member : discord.Member, role : discord.Role):
    await member.add_roles(role)
    
keep_alive()
client.run(os.getenv('fessortoken'))
