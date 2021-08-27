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
        assignment_data = lektiescan(False)
        selection = []
        with open("data/scans.json", "r") as file:
            data = json.load(file)
        try:
            for i in enumerate(assignment_data['beskrivelse']):
                i = i[0]
                if assignment_data['beskrivelse'][i] in data['scans']['beskrivelse']:
                    continue
                data['scans']['begivenhed'].append(assignment_data['begivenhed'][i])
                data['scans']['beskrivelse'].append(assignment_data['beskrivelse'][i])
                data['scans']['author'].append(assignment_data['author'][i])
                data['scans']['files'].append(assignment_data['files'][i])
                data['scans']['tidspunkt'].append(assignment_data['tidspunkt'][i])
                data['scans']['file_names'].append(assignment_data['file_names'][i])
                data['scans']['url'].append(assignment_data['url'][i])
                selection.append(i)
        except KeyError:
            data['scans']['begivenhed'] = []
            data['scans']['beskrivelse'] = []
            data['scans']['author'] = []
            data['scans']['files'] = []
            data['scans']['tidspunkt'] = []
            data['scans']['file_names'] = []
            for i in enumerate(assignment_data['beskrivelse']):
                if assignment_data['beskrivelse'][i] in data['scans']['beskrivelse']:
                    continue
                data['scans']['begivenhed'].append(assignment_data['begivenhed'][i])
                data['scans']['beskrivelse'].append(assignment_data['beskrivelse'][i])
                data['scans']['author'].append(assignment_data['author'][i])
                data['scans']['files'].append(assignment_data['files'][i])
                data['scans']['tidspunkt'].append(assignment_data['tidspunkt'][i])
                data['scans']['file_names'].append(assignment_data['file_names'][i])
                data['scans']['url'].append(assignment_data['url'][i])
                selection.append(i)


        with open("data/scans.json", "w") as file:
            json.dump(data, file, indent=4)

        if selection == []:
            return
        channel = self.bot.get_channel(816693284147691530)
        await self.autopost(channel, assignment_data, selection)

    async def autopost(self, channel, assignment_data, selection):
        """This function formats the data as an embed then posts it in a specific channel"""
        with open("configs/assets.json", "r") as file:
            data = json.load(file)
        for i in selection:
            current_class = assignment_data['begivenhed'][i]
            try:
                embed_color = options.scanColors[current_class]
            except KeyError:
                embed_color = 0xFF5733
            current_teacher = assignment_data['author'][i]
            try:
                embed_thumbnail = data["teachers"][current_teacher.split()[4].lower()]
            except:
                embed_thumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"
                raise
            for_loop_files = [
                assignment_data['files'][i].split(',')[j]
                for j in range(len(assignment_data['files'][i].split(',')))
            ]

            for_loop_file_names = [
                assignment_data['file_names'][i].split(',')[j]
                for j in range(len(assignment_data['file_names'][i].split(',')))
            ]

            file_output = ""
            for k in enumerate(for_loop_files):
                file_output = file_output + "[" + for_loop_file_names[k] + "](" + for_loop_files[k] + ")\n"
            embed=discord.Embed(title=assignment_data['begivenhed'][i], description=assignment_data['tidspunkt'][i], color=embed_color, url=assignment_data['url'][i])
            embed.add_field(name="Description", value=assignment_data['beskrivelse'][i], inline=True)
            embed.set_footer(text=f"{assignment_data['author'][i]}")
            embed.add_field(name="Filer", value=file_output, inline=True)
            embed.set_thumbnail(url=embed_thumbnail)
            print('embed %d created, sending embed' % selection)
            await channel.send('@everyone ny lektie!')
            await channel.send(embed=embed)

    async def post(self, ctx, assignment_data, selection):
        """Formats assignment data to an embed then posts it to the channel in which the scan command was used"""
        with open("configs/assets.json", "r") as file:
            data = json.load(file)
        print('post() called')
        try:
            print(selection[0])
        except IndexError:
            print('poop')
            return "fail"
        for i in selection:
            current_class = assignment_data['begivenhed'][i]
            try:
                embed_color = options.scanColors[current_class]
            except KeyError:
                embed_color = 0xFF5733
            current_teacher = assignment_data['author'][i]
            try:
                embed_thumbnail = data["teachers"][current_teacher.split()[4].lower()]
            except:
                embed_thumbnail = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/200px-Question_mark_%28black%29.svg.png"
                raise
            for_loop_files = [
                assignment_data['files'][i].split(',')[j]
                for j in range(len(assignment_data['files'][i].split(',')))
            ]

            for_loop_file_names = [
                assignment_data['file_names'][i].split(',')[j]
                for j in range(len(assignment_data['file_names'][i].split(',')))
            ]

            file_output = ""
            for k in enumerate(for_loop_files):
                k = k[0]
                file_output = file_output + "[" + for_loop_file_names[k] + "](" + for_loop_files[k] + ")\n"
            embed=discord.Embed(title=assignment_data['begivenhed'][i], description=assignment_data['tidspunkt'][i], color=embed_color, url=assignment_data['url'][i])
            embed.add_field(name="Description", value=assignment_data['beskrivelse'][i], inline=True)
            embed.set_footer(text=f"{assignment_data['author'][i]}")
            embed.add_field(name="Files", value=file_output, inline=True)
            embed.set_thumbnail(url=embed_thumbnail)
            print(f'embed {i} created, sending embed')
            await ctx.send(embed=embed)
        return "success"

    @cog_ext.cog_subcommand(base="schedule",
                        description="Show the schedule for a given day",
                        name="day",
                        guild_ids=functions.utils.servers,
                        base_default_permission=True,
                        base_permissions=functions.utils.slash_perms("banned"),
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
        """Relays the schedule of a specific day"""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
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
        except KeyError:
            await ctx.send(embed=discord.Embed(title='Invalid day', description="Might tomorrow be a saturday or a sunday?"), hidden=ephemeral)

    @cog_ext.cog_subcommand(base="schedule", name="today", description="Show today's schedule.", guild_ids=functions.utils.servers, options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _schedule_today(self, ctx: discord_slash.SlashContext, **kwargs):
        """Relays the current day's schedule; defaults to monday if it's a weekend"""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        today = datetime.datetime.today().weekday()
        if today >= 5:
            await ctx.send('Today is not a weekday, assuming monday.', hidden=ephemeral)
            today = 0
        today = str(today)
        output = options.schedules[today]
        await ctx.send(output, hidden=ephemeral)

    async def scan(self, ctx: discord_slash.SlashContext, **kwargs):
        """Function that obtains raw data from the lektiescanner function and formats the text, then calls post"""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        try:
            await ctx.defer(hidden=ephemeral)
            assignment_data = lektiescan(True)
            if kwargs["mode"] == "all":
                lektie_list = [
                    str(i + 1)
                    + ". "
                    + assignment_data['begivenhed'][i]
                    + " | Afleveres "
                    + assignment_data['tidspunkt'][i]
                    for i in range(len(assignment_data['begivenhed']))
                ]

                description = "\n\n".join(lektie_list)
                field_2 = "Use the command again with a different mode to see full assignments"
                embed=discord.Embed(title="Found %d assignments" % len(assignment_data['begivenhed']), description=description, color=0xFF0000)
                embed.add_field(name="What now?", value=field_2)
                await ctx.send(embed=embed)
                return
            if kwargs["mode"] == "subject":
                num_list = [
                    i
                    for i in range(len(assignment_data['begivenhed']))
                    if kwargs["parameters"] in assignment_data['begivenhed'][i]
                ]

                user_input = num_list
            elif kwargs["mode"] == "date":
                if kwargs["parameters"] == "tomorrow":
                    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                    tomorrow = tomorrow.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
                    user_input = tomorrow
                    num_list = [i for i in range(len(assignment_data['tidspunkt'])) if str(assignment_data['user_input']) in assignment_data['tidspunkt'][i]]
                elif kwargs["parameters"] in options.translations.keys() or kwargs["parameters"] in options.translations.values():
                    weekday = datetime.datetime.today().weekday()
                    if kwargs["parameters"] in options.translations.keys():
                        kwargs["parameters"] = options.translations[kwargs["parameters"]]
                    diff = weekday - int(options.conversions[kwargs["parameters"]])
                    target_date = datetime.date.today() - datetime.timedelta(days=diff)
                    target_date = target_date.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
                    user_input = target_date
                    num_list = [i for i in range(len(assignment_data['tidspunkt'])) if str(user_input) in assignment_data['tidspunkt'][i]]
                else:
                    num_list = [
                        i
                        for i in range(len(assignment_data['begivenhed']))
                        if str(kwargs["parameters"]) in assignment_data['tidspunkt'][i]
                    ]

                user_input = num_list
            elif kwargs["mode"] == "teacher":
                num_list = [
                    i
                    for i in range(len(assignment_data['author']))
                    if str(kwargs["parameters"]) in assignment_data['author'][i]
                ]

                user_input = num_list
            if str(user_input) == "[]":
                await ctx.send(embed=discord.Embed(title='Ingen lektier fundet :weary:', description='', color=0xFF0000))
                return
            try:
                await self.post(ctx, assignment_data, user_input)
            except:
                await ctx.send(embed=discord.Embed(title="EPIC FAIL :rofl:", description="Du skal skrive et tal, der passer til de lektier, botten har fundet!!!!! :rage::rage::rage:"))
                raise
        except:
            await ctx.send(embed=discord.Embed(title="Scan fejlede.", description="", color=0xFF0000))
            raise

    @cog_ext.cog_subcommand(base="scan", name="all", description="Scan for an index of all assignments on Viggo.", guild_ids=functions.utils.servers, base_default_permission=False, base_permissions=functions.utils.slash_perms("lektiescan"), options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_all(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="all", private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="subject", description="Scan for assignments from a specific subject on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="subject", description="Which subject?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_subject(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="subject", parameters=kwargs["subject"], private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="date", description="Scan for assignments from a specific date on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="date", description="Which date?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_date(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="date", parameters=kwargs["date"], private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="teacher", description="Scan for assignments from a specific teacher on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="teacher", description="Which teacher?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_teacher(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral=functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="teacher", parameters=kwargs["teacher"], private=ephemeral)


def setup(bot):
    """Adds the cog"""
    bot.add_cog(Skole(bot))
