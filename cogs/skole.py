"""Adds school related commands to relay assignments and schedules."""
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
    """The skole cog."""
    def __init__(self, bot):
        self.bot = bot # pylint: disable=no-member
        self.scan_loop.start() # pylint: disable=no-member

    def cog_unload(self):
        """Unloads the cog."""
        self.scan_loop.cancel() # pylint: disable=no-member


    @tasks.loop(minutes=5.0)
    async def scan_loop(self):
        """Runs every five minutes and checks if the lektiescanner's output is different from the last."""
        assignment_data = lektiescan()
        selection = []
        with open("data/scans.json", "r") as file:
            data = json.load(file)
        try:
            for i in enumerate(assignment_data['description']):
                i = i[0]
                if assignment_data['description'][i] in data['scans']['description']:
                    continue
                data['scans']['subject'].append(assignment_data['subject'][i])
                data['scans']['description'].append(assignment_data['description'][i])
                data['scans']['author'].append(assignment_data['author'][i])
                data['scans']['files'].append(assignment_data['files'][i])
                data['scans']['time'].append(assignment_data['time'][i])
                data['scans']['file_names'].append(assignment_data['file_names'][i])
                data['scans']['url'].append(assignment_data['url'][i])
                selection.append(i)
        except KeyError:
            data['scans']['subject'] = []
            data['scans']['description'] = []
            data['scans']['author'] = []
            data['scans']['files'] = []
            data['scans']['time'] = []
            data['scans']['file_names'] = []
            for i in enumerate(assignment_data['description']):
                i = i[0]
                if assignment_data['description'][i] in data['scans']['description']:
                    continue
                data['scans']['subject'].append(assignment_data['subject'][i])
                data['scans']['description'].append(assignment_data['description'][i])
                data['scans']['author'].append(assignment_data['author'][i])
                data['scans']['files'].append(assignment_data['files'][i])
                data['scans']['time'].append(assignment_data['time'][i])
                data['scans']['file_names'].append(assignment_data['file_names'][i])
                data['scans']['url'].append(assignment_data['url'][i])
                selection.append(i)


        with open("data/scans.json", "w") as file:
            json.dump(data, file, indent=4)

        if selection == []:
            return
        channel = self.bot.get_channel(816693284147691530)
        await self.post(channel, assignment_data, selection)

    @staticmethod
    async def post(ctx, assignment_data, selection):
        """Formats assignment data to an embed then posts it to the channel in which the scan command was used."""
        with open("configs/assets.json", "r") as file:
            data = json.load(file)
        try:
            print(selection[0])
        except IndexError:
            return "fail"
        for i in selection:
            current_class = assignment_data['subject'][i]
            try:
                embed_color = options.scanColors[current_class]
            except KeyError:
                embed_color = 0xFF5733
            current_teacher = assignment_data['author'][i]
            try:
                embed_thumbnail = data['teachers'][current_teacher.replace(" ".join(current_teacher.split(' ')[:4]), '').lstrip().lower()]
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
            embed = discord.Embed(title=assignment_data['subject'][i], description=assignment_data['time'][i], color=embed_color, url=assignment_data['url'][i])
            embed.add_field(name="Description", value=assignment_data['description'][i], inline=True)
            embed.set_footer(text=f"{assignment_data['author'][i]}")
            embed.add_field(name="Files", value=file_output, inline=True)
            embed.set_thumbnail(url=embed_thumbnail)
            await ctx.send(embed=embed)
        return "success"

    @cog_ext.cog_subcommand(
        base="schedule",
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
        """Relays the schedule of a specific day."""
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

    @cog_ext.cog_subcommand(
        base="schedule",
        name="today",
        description="Show today's schedule.",
        guild_ids=functions.utils.servers,
        options=[
            create_option(
                name="private",
                description="send the message privately?",
                option_type=5,
                required=False
            )
        ]
    )
    async def _schedule_today(self, ctx: discord_slash.SlashContext, **kwargs):
        """Relays the current day's schedule; defaults to monday if it's a weekend."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        today = datetime.datetime.today().weekday()
        if today >= 5:
            await ctx.send('Today is not a weekday, assuming monday.', hidden=ephemeral)
            today = 0
        today = str(today)
        output = options.schedules[today]
        await ctx.send(output, hidden=ephemeral)

    async def send_all(self, ctx: discord_slash.SlashContext, assignment_data):
        """Sends all assignments in one embed; doesn't send descriptions."""
        lektie_list = [
            str(i + 1)
            + ". "
            + assignment_data['subject'][i]
            + " | Afleveres "
            + assignment_data['time'][i]
            for i in range(len(assignment_data['subject']))
        ]

        description = "\n\n".join(lektie_list)
        field_2 = "Use the command again with a different mode to see full assignments"
        embed = discord.Embed(title="Found %d assignments" % len(assignment_data['subject']), description=description, color=0xFF0000)
        embed.add_field(name="What now?", value=field_2)
        await ctx.send(embed=embed)
        return

    @staticmethod
    def find_subjects(assignment_data, parameters):
        """Finds assignments of a specific subject."""
        return [
            i
            for i in range(len(assignment_data['subject']))
            if parameters in assignment_data['subject'][i]
        ]

    @staticmethod
    def find_dates(assignment_data, parameters):
        """Finds assignments from a specific date."""
        if parameters == "tomorrow":
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
            user_input = tomorrow
            return [
                i
                for i in range(len(assignment_data['time']))
                if str(assignment_data['user_input']) in assignment_data['time'][i]
            ]

        if (
            parameters not in options.translations.keys()
            and parameters not in options.translations.values()
        ):
            return [
                i
                for i in range(len(assignment_data['subject']))
                if str(parameters) in assignment_data['time'][i]
            ]

        weekday = datetime.datetime.today().weekday()
        if parameters in options.translations.keys():
            parameters = options.translations[parameters]
        diff = weekday - int(options.conversions[parameters])
        target_date = datetime.date.today() - datetime.timedelta(days=diff)
        target_date = target_date.strftime("%d. %b").replace('May', 'Maj').replace('Oct', 'Okt').replace('0', '').lower()
        user_input = target_date
        return [
            i
            for i in range(len(assignment_data['time']))
            if str(user_input) in assignment_data['time'][i]
        ]

    @staticmethod
    def find_teacher(assignment_data, parameters):
        """Finds assignments from a specific teacher."""
        return [
            i
            for i in range(len(assignment_data['author']))
            if str(parameters) in assignment_data['author'][i]
        ]

    async def handle_mode(self, ctx, assignment_data, mode, parameters):
        """Handles mode and parameters to know what to look for."""
        if mode == "all":
            await self.send_all(ctx, assignment_data)
            return None
        if mode == "subject":
            user_input = self.find_subjects(assignment_data, parameters)
        elif mode == "date":
            user_input = self.find_dates(assignment_data, parameters)
        elif mode == "teacher":
            user_input = self.find_teacher(assignment_data, parameters)
        return user_input

    async def scan(self, ctx: discord_slash.SlashContext, **kwargs):
        """Function that obtains raw data from the lektiescanner function and formats the text, then calls post."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        if 'parameters' not in kwargs:
            kwargs['parameters'] = None
        try:
            await ctx.defer(hidden=ephemeral)
            assignment_data = lektiescan()
            user_input = await self.handle_mode(ctx, assignment_data, kwargs['mode'], kwargs['parameters'])
            if str(user_input) == "[]":
                await ctx.send(embed=discord.Embed(title='No assignments found :weary:', color=0xFF0000))
                return
            if user_input is None:
                return
            await self.post(ctx, assignment_data, user_input)
        except Exception as error:
            await ctx.send(
                embed=discord.Embed(
                    title='Scan failed.',
                    description=f'Exception:\n```\n{error}\n```',
                    color=16711680,
                )
            )
            raise

    @cog_ext.cog_subcommand(base="scan", name="all", description="Scan for an index of all assignments on Viggo.", guild_ids=functions.utils.servers, base_default_permission=False, base_permissions=functions.utils.slash_perms("lektiescan"), options=[create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_all(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="all", private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="subject", description="Scan for assignments from a specific subject on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="subject", description="Which subject?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_subject(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="subject", parameters=kwargs["subject"], private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="date", description="Scan for assignments from a specific date on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="date", description="Which date?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_date(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="date", parameters=kwargs["date"], private=ephemeral)

    @cog_ext.cog_subcommand(base="scan", name="teacher", description="Scan for assignments from a specific teacher on Viggo.", guild_ids=functions.utils.servers, options=[create_option(name="teacher", description="Which teacher?", option_type=3, required=True), create_option(name="private", description="send the message privately?", option_type=5, required=False)])
    async def _scan_teacher(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        await self.scan(ctx, mode="teacher", parameters=kwargs["teacher"], private=ephemeral)


def setup(bot):
    """Adds the cog."""
    bot.add_cog(Skole(bot))
