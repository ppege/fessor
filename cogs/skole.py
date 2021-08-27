# pylint: disable=line-too-long, unspecified-encoding
"""This cog adds school related commands to relay assignments and schedules"""
import json
import datetime
import discord
from discord.ext import commands, tasks
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
import functions.utils # pylint: disable=import-error
from configs import options # pylint: disable=import-error
from functions.school.lektiescanner import lektiescan # pylint: disable=import-error

class Skole(commands.Cog):
    """The skole cog"""
    def __init__(self, bot):
        self.bot = bot # pylint: disable=no-member
        self.scan_loop.start() # pylint: disable=no-member

    def cog_unload(self):
        self.scan_loop.cancel() # pylint: disable=no-member


    @tasks.loop(minutes=5.0)
    async def scan_loop(self):
        """This function runs every five minutes and checks if the lektiescanner's output is different from the last"""
        begivenhed, beskrivelse, author, files, tidspunkt, file_names, url = lektiescan(False)
        selection = []
        with open("data/scans.json", "r") as file:
            data = json.load(file)
        try:
            for i in enumerate(beskrivelse):
                if beskrivelse[i] in data['scans']['beskrivelse']:
                    continue
                data['scans']['begivenhed'].append(begivenhed[i])
                data['scans']['beskrivelse'].append(beskrivelse[i])
                data['scans']['author'].append(author[i])
                data['scans']['files'].append(files[i])
                data['scans']['tidspunkt'].append(tidspunkt[i])
                data['scans']['file_names'].append(file_names[i])
                data['scans']['url'].append(url[i])
                selection.append(i)
        except:
            data['scans']['begivenhed'] = []
            data['scans']['beskrivelse'] = []
            data['scans']['author'] = []
            data['scans']['files'] = []
            data['scans']['tidspunkt'] = []
            data['scans']['file_names'] = []
            data['scans']['url'] = []
            for i in enumerate(beskrivelse):
                if beskrivelse[i] in data['scans']['beskrivelse']:
                    continue
                data['scans']['begivenhed'].append(begivenhed[i])
                data['scans']['beskrivelse'].append(beskrivelse[i])
                data['scans']['author'].append(author[i])
                data['scans']['files'].append(files[i])
                data['scans']['tidspunkt'].append(tidspunkt[i])
                data['scans']['file_names'].append(file_names[i])
                data['scans']['url'].append(url[i])
                selection.append(i)


        with open("data/scans.json", "w") as file:
            json.dump(data, file, indent=4)

        if selection == []:
            return
        channel = self.bot.get_channel(816693284147691530)
        await self.autopost(channel, begivenhed, beskrivelse, author, files, tidspunkt, file_names, selection, url)

    async def autopost(self, channel, begivenhed, beskrivelse, author, files, tidspunkt, file_names, selection, url):
        """This function formats the data as an embed then posts it in a specific channel"""
        with open("configs/assets.json", "r") as file:
            data = json.load(file)
        for i in selection:
            currentClass = begivenhed[i]
            currentTeacher = author[i]
            try:
                embedColor = options.scanColors[currentClass]
            except:
                embedColor = 0xFF5733
            if 1 == 1:
                try:
                    embedThumbnail = data["teachers"][currentTeacher.split()[4].lower()]
                except:
                    embedThumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"
                    raise
                forLoopFiles = [
                    files[i].split(',')[j]
                    for j in range(len(files[i].split(',')))
                ]

                forLoopfile_names = [
                    file_names[i].split(',')[j]
                    for j in range(len(file_names[i].split(',')))
                ]

                fileOutput = ""
                for k in enumerate(forLoopFiles):
                    fileOutput = fileOutput + "[" + forLoopfile_names[k] + "](" + forLoopFiles[k] + ")\n"
                embed=discord.Embed(title=begivenhed[i], description=tidspunkt[i], color=embedColor, url=url[i])
                embed.add_field(name="Beskrivelse", value=beskrivelse[i], inline=True)
                embed.set_footer(text=f"{author[i]}")
                embed.add_field(name="Filer", value=fileOutput, inline=True)
                embed.set_thumbnail(url=embedThumbnail)
                print('embed %d created, sending embed' % selection)
                await channel.send('@everyone ny lektie!')
                await channel.send(embed=embed)

    async def post(self, ctx, begivenhed, beskrivelse, author, files, tidspunkt, file_names, selection, url):
        with open("configs/assets.json", "r") as file:
            data = json.load(file)
        print('post() called')
        try:
            print(selection[0])
        except:
            print('poop')
            return "fail"
        for i in selection:
            currentClass = begivenhed[i]
            currentTeacher = author[i]
            try:
                embedColor = options.scanColors[currentClass]
            except:
                embedColor = 0xFF5733
            if 1 == 1:
                try:
                    embedThumbnail = data["teachers"][currentTeacher.split()[4].lower()]
                except:
                    embedThumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"
                    raise
                forLoopFiles = [
                    files[i].split(',')[j]
                    for j in range(len(files[i].split(',')))
                ]

                forLoopfile_names = [
                    file_names[i].split(',')[j]
                    for j in range(len(file_names[i].split(',')))
                ]

                fileOutput = ""
                for k in enumerate(forLoopFiles):
                    k = k[0]
                    fileOutput = fileOutput + "[" + forLoopfile_names[k] + "](" + forLoopFiles[k] + ")\n"
                embed=discord.Embed(title=begivenhed[i], description=tidspunkt[i], color=embedColor, url=url[i])
                embed.add_field(name="Beskrivelse", value=beskrivelse[i], inline=True)
                embed.set_footer(text=f"{author[i]}")
                embed.add_field(name="Filer", value=fileOutput, inline=True)
                embed.set_thumbnail(url=embedThumbnail)
                print(f'embed {i} created, sending embed')
                await ctx.send(embed=embed)
        return "success"

    @cog_ext.cog_subcommand(base="schedule",
                        description="Show the schedule for a given day",
                        name="day",
                        guild_ids=functions.utils.servers,
                        base_default_permission=True,
                        base_permissions=functions.utils.slPerms("banned"),
                        options=[
                          create_option(
                            name="day",
                            description="Which day's schedule?",
                            option_type=3,
                            required=True
                          ),
                          create_option(
                            name="private",
                            description="send the message privately?",
                            option_type=5,
                            required=False
                          )
                        ]
                    )
    async def schedule(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        day = kwargs["day"]
        try:
            if day in options.dayList:
                await ctx.send(options.skemaer[day], hidden=ephemeral)
            elif day == "tomorrow":
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                tomorrow = tomorrow.weekday()
                await ctx.send(options.skemaer[options.dayList[tomorrow]], hidden=ephemeral)
            else:
                await ctx.send(embed=discord.Embed(title='Invalid input', description='Du skal enten angive en ugedag eller `tomorrow`.'), hidden=ephemeral)
        except:
            description = 'Det her burde VIRKELIG ikke være her.'
            if day == "tomorrow":
                description = 'Er det mon en lørdag eller en søndag i morgen?'
            else:
                description = 'Sig lige til William, at han skal checke terminalen. Jeg har printet fejlen ud der.'
                raise
            await ctx.send(embed=discord.Embed(title='Invalid dag', description=description), hidden=ephemeral)

    @cog_ext.cog_subcommand(base="schedule", name="today", description="Show today's schedule.", guild_ids=functions.utils.servers, options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _schedule_today(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        today = datetime.datetime.today().weekday()
        if today >= 5:
            await ctx.send('Today is not a weekday, assuming monday.', hidden=ephemeral)
            today = 0
        today = str(today)
        output = options.schedules[today]
        await ctx.send(output, hidden=ephemeral)

    async def scan(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        try:
            await ctx.defer(hidden=ephemeral)
            begivenhed, beskrivelse, author, files, tidspunkt, file_names, url = lektiescan(True)
            if kwargs["mode"] == "all":
                lektieList = [
                    str(i + 1)
                    + ". "
                    + begivenhed[i]
                    + " | Afleveres "
                    + tidspunkt[i]
                    for i in range(len(begivenhed))
                ]

                description = "\n\n".join(lektieList)
                Field2 = "Use the command again with a different mode to see full assignments"
                embed=discord.Embed(title="Found %d assignments" % len(begivenhed), description=description, color=0xFF0000)
                embed.add_field(name="What now?", value=Field2)
                await ctx.send(embed=embed)
                return
            else:
                if kwargs["mode"] == "subject":
                    numList = [
                        i
                        for i in range(len(begivenhed))
                        if kwargs["parameters"] in begivenhed[i]
                    ]

                    userInput = numList
                elif kwargs["mode"] == "date":
                    if kwargs["parameters"] == "tomorrow":
                        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                        tomorrow = tomorrow.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
                        userInput = tomorrow
                        numList = [i for i in range(len(tidspunkt)) if str(userInput) in tidspunkt[i]]
                    elif kwargs["parameters"] in options.translations.keys() or kwargs["parameters"] in options.translations.values():
                        weekday = datetime.datetime.today().weekday()
                        if kwargs["parameters"] in options.translations.keys():
                            kwargs["parameters"] = options.translations[kwargs["parameters"]]
                        diff = weekday - int(options.conversions[kwargs["parameters"]])
                        targetDate = datetime.date.today() - datetime.timedelta(days=diff)
                        targetDate = targetDate.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
                        userInput = targetDate
                        numList = [i for i in range(len(tidspunkt)) if str(userInput) in tidspunkt[i]]
                    else:
                        numList = [
                            i
                            for i in range(len(begivenhed))
                            if str(kwargs["parameters"]) in tidspunkt[i]
                        ]

                    userInput = numList
                elif kwargs["mode"] == "teacher":
                    numList = [
                        i
                        for i in range(len(author))
                        if str(kwargs["parameters"]) in author[i]
                    ]

                    userInput = numList
            if str(userInput) == "[]":
                await ctx.send(embed=discord.Embed(title='Ingen lektier fundet :weary:', description='', color=0xFF0000))
                return
            try:
                await self.post(ctx, begivenhed, beskrivelse, author, files, tidspunkt, file_names, userInput, url)
            except:
                await ctx.send(embed=discord.Embed(title="EPIC FAIL :rofl:", description="Du skal skrive et tal, der passer til de lektier, botten har fundet!!!!! :rage::rage::rage:"))
                raise
        except:
            await ctx.send(embed=discord.Embed(title="Scan fejlede.", description="", color=0xFF0000))
            raise

    @cog_ext.cog_subcommand(base="scan", name="all", description="Scan for an index of all assignments on Viggo.", guild_ids=functions.utils.servers, base_default_permission=False, base_permissions=functions.utils.slPerms("lektiescan"), options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_all(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.eCheck(**kwargs)
        await self.scan(ctx, mode="all", private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="subject", description="Scan for assignments from a specific subject on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="subject", description="Which subject?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_subject(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.eCheck(**kwargs)
        await self.scan(ctx, mode="subject", parameters=kwargs["subject"], private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="date", description="Scan for assignments from a specific date on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="date", description="Which date?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_date(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.eCheck(**kwargs)
        await self.scan(ctx, mode="date", parameters=kwargs["date"], private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="teacher", description="Scan for assignments from a specific teacher on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="teacher", description="Which teacher?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_teacher(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.eCheck(**kwargs)
        await self.scan(ctx, mode="teacher", parameters=kwargs["teacher"], private=ephemeral)


def setup(bot):
    bot.add_cog(Skole(bot))
