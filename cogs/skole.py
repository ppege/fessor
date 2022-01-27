"""Adds school related commands to relay assignments and schedules."""
import json
import datetime
import configparser
import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from viggoscrape import Viggoscrape
import functions.utils # pylint: disable=import-error
from configs import options # pylint: disable=import-error

class Skole(commands.Cog):
    """The skole cog."""
    def __init__(self, bot):
        self.bot = bot # pylint: disable=no-member
        config = configparser.ConfigParser()
        config.read('cred.ini')
        self.scraper = Viggoscrape(
            subdomain="nr-aadal",
            username=config['config']['USERNAME'],
            password=config['config']['PASSWORD']
        )

    @staticmethod
    async def post(ctx, assignment_data):
        """Formats assignment data to an embed then posts it to the channel in which the scan command was used."""
        with open("configs/assets.json", "r") as file:
            assets = json.load(file)
        embeds = []
        for assignment in assignment_data:
            current_class = assignment['subject']
            embed_color = options.scanColors[current_class] if current_class in options.scanColors else 0xFF5733
            author = assignment['author']
            current_teacher = author.replace(" ".join(author.split(' ')[:4]), '').lstrip()
            embed_thumbnail = assets['teachers'].get(current_teacher.lower())
            if embed_thumbnail is None:
                embed_thumbnail = "https://st3.depositphotos.com/4111759/13425/v/600/depositphotos_134255634-stock-illustration-avatar-icon-male-profile-gray.jpg"

            embed = discord.Embed(title=assignment['subject'], description=f"**Due on {assignment['date']}**\n{assignment['description']}", color=embed_color, url=assignment['url'])
            embed.set_footer(text=f"{author}", icon_url=embed_thumbnail)
            embeds.append(embed)
        for i, embed in enumerate(embeds):
            if i == 0:
                await ctx.send(embed=embed)
            else:
                await ctx.channel.send(embed=embed)

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
            + assignment['subject']
            + " | Due on "
            + assignment['date']
            for i, assignment in enumerate(assignment_data)
        ]

        description = "\n\n".join(lektie_list)
        field_2 = "Use the command with search to see full assignments"
        embed = discord.Embed(title=f'Found {len(assignment_data)} assignments', description=description, color=0xFF0000)
        embed.add_field(name="What now?", value=field_2)
        await ctx.send(embed=embed)
        return

    def filter_search(self, data, search):
        """Use viggoscrape to get assignment data"""
        def match_search(assignment):
            return any(search in value for value in assignment.values())
        return list(filter(match_search, data))

    @cog_ext.cog_slash(
        name="homework",
        description="Check if there's homework due",
        guild_ids=functions.utils.servers,
        default_permission=False,
        permissions=functions.utils.slash_perms("lektiescan"),
        options=[
            create_option(
                name="search",
                description="Which teacher, subject, day, etc.",
                option_type=3,
                required=False
            )
        ]
    )
    async def homework(self, ctx: discord_slash.SlashContext, **kwargs):
        """Command to get assignments, powered by viggoscrape"""
        data = self.scraper.get_assignments()
        if "errors" in data:
            ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description="\n".join(data["errors"]),
                    color=0xFF0000
                )
            )
            return
        searching = False
        if "search" in kwargs:
            data = self.filter_search(data, kwargs["search"])
            searching = True
        if data == []:
            await ctx.send(embed=discord.Embed(title="No assignments found."))
            return
        match searching:
            case True:
                await self.post(ctx, data)
            case False:
                await self.send_all(ctx, data)
            case _:
                await ctx.send(embed=discord.Embed(title="Critical error?!?! check logs :rage:"))

def setup(bot):
    """Adds the cog."""
    bot.add_cog(Skole(bot))
