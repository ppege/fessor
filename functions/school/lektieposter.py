import discord
import os
import discord.ext.commands
from discord.ext import commands


bot = commands.Bot(command_prefix='.')

print('que2?!?')

async def post(ctx, begivenhed, beskrivelse, author, files, tidspunkt, fileNames):
  print('post() called')
  for i in range(0, len(begivenhed)):
    currentClass = begivenhed[i]
    currentTeacher = author[i]
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
        for j in range(0, len(files[i].split(','))):
          forLoopFiles.append(files[i].split(',')[j])
        forLoopFileNames = []
        for j in range(0, len(fileNames[i].split(','))):
          forLoopFileNames.append(fileNames[i].split(',')[j])
        fileOutput = ""
        for k in range(0, len(forLoopFiles)):
          fileOutput = fileOutput + "[" + forLoopFileNames[k] + "](" + forLoopFiles[k] + ")\n"
        embed=discord.Embed(title=begivenhed[i], description=tidspunkt[i], color=embedColor)
        embed.add_field(name="Beskrivelse", value=beskrivelse[i], inline=True)
        embed.set_footer(text=author[i])
        embed.add_field(name="Filer", value=fileOutput, inline=True)
        embed.set_thumbnail(url=embedThumbnail)
        await ctx.send(embed=embed)
        return


bot.run(os.getenv('fessortoken'))