import discord
from discord.ext import commands, tasks
import functions.utils
import datetime
from configs import options
from functions.school.lektiescanner import lektiescan
from dateutil.relativedelta import relativedelta
import json
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

class Skole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scanLoop.start()

    def cog_unload(self):
        self.scanLoop.cancel()


    @tasks.loop(minutes=5.0)
    async def scanLoop(self):
        begivenhed, beskrivelse, author, files, tidspunkt, fileNames, url = lektiescan(False)
        selection = []
        with open("data/scans.json", "r") as file:
            data = json.load(file)
        try:
            for i in range(len(beskrivelse)):
                if beskrivelse[i] in data['scans']['beskrivelse']:
                    continue
                data['scans']['begivenhed'].append(begivenhed[i])
                data['scans']['beskrivelse'].append(beskrivelse[i])
                data['scans']['author'].append(author[i])
                data['scans']['files'].append(files[i])
                data['scans']['tidspunkt'].append(tidspunkt[i])
                data['scans']['fileNames'].append(fileNames[i])
                data['scans']['url'].append(url[i])
                selection.append(i)
        except:
            data['scans']['begivenhed'] = []
            data['scans']['beskrivelse'] = []
            data['scans']['author'] = []
            data['scans']['files'] = []
            data['scans']['tidspunkt'] = []
            data['scans']['fileNames'] = []
            data['scans']['url'] = []
            for i in range(len(beskrivelse)):
                if beskrivelse[i] in data['scans']['beskrivelse']:
                    continue
                data['scans']['begivenhed'].append(begivenhed[i])
                data['scans']['beskrivelse'].append(beskrivelse[i])
                data['scans']['author'].append(author[i])
                data['scans']['files'].append(files[i])
                data['scans']['tidspunkt'].append(tidspunkt[i])
                data['scans']['fileNames'].append(fileNames[i])
                data['scans']['url'].append(url[i])
                selection.append(i)


        with open("data/scans.json", "w") as file:
            json.dump(data, file, indent=4)

        if selection == []:
            return
        else:
            channel = self.bot.get_channel(816693284147691530)
            await self.post(channel, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, selection, url)

    async def autopost(self, channel, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, selection, url):
        with open("data/scans.json", "r") as file:
            data = json.load(file)
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
                  embedThumbnail = data["teachers"][embedThumbnail]
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
                await channel.send('@everyone ny lektie!')
                await channel.send(embed=embed)

    async def post(self, ctx, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, selection, url):
          with open("configs/assets.json", "r") as file:
            data = json.load(file)
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
                    embedThumbnail = data["teachers"][embedThumbnail]
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

    @functions.utils.banned()
    @commands.command()
    async def skema(self, ctx, *args):
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
            if args[0] in options.dayList:
              await ctx.send(options.skemaer[args[0]])
            elif args[0] == "tomorrow":
              tomorrow = datetime.date.today() + datetime.timedelta(days=1)
              tomorrow = tomorrow.weekday()
              await ctx.send(options.skemaer[options.dayList[tomorrow]])
            else:
              await ctx.send(embed=discord.Embed(title='Invalid input', description='Du skal enten angive en ugedag eller `tomorrow`.'))
          except:
            description = 'Det her burde VIRKELIG ikke være her.'
            if args[0] == "tomorrow":
              description = 'Er det mon en lørdag eller en søndag i morgen?'
            else:
              description = 'Sig lige til William, at han skal checke terminalen. Jeg har printet fejlen ud der.'
              raise
            await ctx.send(embed=discord.Embed(title='Invalid dag', description=description))

    @functions.utils.lektiescan()
    @commands.command()
    async def overview(self, ctx, *args):
      try:
        if len(args) == 0:
          await ctx.send(embed=discord.Embed(title='Ingen input', description=''))
        elif len(args) > 1 and (args[0] == "tomorrow" or args[0] == "today"):
          await ctx.send(embed=discord.Embed(title='For mange args', description='Denne kommando tager kun 1 argument.\nValide argumenter: `tomorrow`, `today`, `[dato]`'))
        else:
          userInput = " ".join(args)
          if userInput == "tomorrow":
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            tomorrowF = tomorrow.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
            weekday = options.dayList[tomorrow.weekday()]
            output = [tomorrow, tomorrowF, weekday]
          elif userInput == "today":
            today = datetime.date.today()
            todayF = today.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
            weekday = options.dayList[today.weekday()]
            output = [today, todayF, weekday]
          else:
            userInput = userInput.lower()
            userInputConv = userInput.replace('maj', 'may').replace('okt', 'oct')
            date_time_obj = datetime.datetime.strptime(userInputConv, '%d. %b')
            date_time_obj = date_time_obj + relativedelta(years=121)
            weekday = options.dayList[date_time_obj.weekday()]
            output = [date_time_obj, userInput, weekday]
          await self.skema(ctx, output[2])
          await self.scan(ctx, "dato", output[1])
      except:
        await ctx.send(embed=discord.Embed(title='Ukendt fejl', description='Jeg er ikke helt sikker på, hvad der gik galt.\nValide argumenter: `tomorrow`, `today`, `[dato]`'))
        raise
    
    scanOptionDict={
      "All posts": "all",
      "Date": "date",
      "Subject": "subject",
      "Teacher": "teacher"
    }

    @functions.utils.lektiescan()
    @cog_ext.cog_slash(name="scan",
                          description="Scan for homework on Viggo (nr-aadal only)",
                          guild_ids=functions.utils.servers,
                          permissions=functions.utils.slPerms("lektiescan"),
                          options=[
                            create_option(
                                name="mode",
                                description="What type of search to make",
                                option_type=3,
                                required=True,
                                choices=[
                                  create_choice(name=key, value=value) for key, value in scanOptionDict.items()
                                ]
                            ),
                            create_option(
                                name="parameters",
                                description="Search parameters for date, subject or teacher",
                                option_type=3,
                                required=False
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                          ]
                    )
    async def scan(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        try:
          await ctx.defer(hidden=ephemeral)
          begivenhed, beskrivelse, author, files, tidspunkt, fileNames, url = lektiescan(True)
          if kwargs["mode"] == "all":
            lektieList = []
            for i in range(0, len(begivenhed)):
              lektieList.append(str(i + 1) + ". " + begivenhed[i] + " | Afleveres " + tidspunkt[i])
            description = "\n\n".join(lektieList)
            Field2 = "Use the command again with a different mode to see full assignments"
            embed=discord.Embed(title="Found %d assignments" % len(begivenhed), description=description, color=0xFF0000)
            embed.add_field(name="What now?", value=Field2)
            await ctx.send(embed=embed)
            return
          else:
            if kwargs["mode"] == "subject":
              numList = []
              for i in range(0, len(begivenhed)):
                if kwargs["parameters"] in begivenhed[i]:
                  numList.append(i)
              userInput = numList
            elif kwargs["mode"] == "date":
              if kwargs["parameters"] == "tomorrow":
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                tomorrow = tomorrow.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
                userInput = tomorrow
                numList = []
                for i in range(0, len(tidspunkt)):
                  if str(userInput) in tidspunkt[i]:
                    numList.append(i)
                userInput = numList
              elif kwargs["parameters"] in ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag']:
                weekday = datetime.datetime.today().weekday()
                diff = weekday - int(options.conversions[kwargs["parameters"]])
                targetDate = datetime.date.today() - datetime.timedelta(days=diff)
                targetDate = targetDate.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
                userInput = targetDate
                numList = []
                for i in range(0, len(tidspunkt)):
                  if str(userInput) in tidspunkt[i]:
                    numList.append(i)
                userInput = numList
              else:
                numList = []
                for i in range(0, len(begivenhed)):
                  if str(kwargs["parameters"]) in tidspunkt[i]:
                    numList.append(i)
                userInput = numList
            elif kwargs["mode"] == "teacher":
              numList = []
              for i in range(0, len(author)):
                if str(kwargs["parameters"]) in author[i]:
                  numList.append(i)
              userInput = numList
          if str(userInput) == "[]":
            await ctx.send(embed=discord.Embed(title='Ingen lektier fundet :weary:', description='', color=0xFF0000))
            return
          try:
            await self.post(ctx, begivenhed, beskrivelse, author, files, tidspunkt, fileNames, userInput, url)
          except:
            await ctx.send(embed=discord.Embed(title="EPIC FAIL :rofl:", description="Du skal skrive et tal, der passer til de lektier, botten har fundet!!!!! :rage::rage::rage:"))
            raise
        except:
          await ctx.send(embed=discord.Embed(title="Scan fejlede.", description="", color=0xFF0000))
          raise



def setup(bot):
    bot.add_cog(Skole(bot))
