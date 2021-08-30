"""Adds several commands that help users look things up."""
import configparser
import discord
from discord.ext import commands
from PyDictionary import PyDictionary
from translate import Translator
import wikipedia
import wolframalpha
from googlesearch import search
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import wait_for_component, create_button, create_actionrow
from discord_slash.model import ButtonStyle
import functions.utils # pylint: disable=import-error


class Lookup(commands.Cog):
    """Lookup cog."""
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="define",
        description="Define a word",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="word",
                description="which word to define?",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption
    )
    async def define(self, ctx: discord_slash.SlashContext, **kwargs):
        """Find definition of a word and relay it in an embed."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        word = kwargs["word"]
        await ctx.defer(hidden=ephemeral)
        dictionary = PyDictionary()
        meaning = dictionary.meaning(word)
        if meaning is None:
            await ctx.send(embed=discord.Embed(title=f"No definition found for {word}", color=0xFF0000))
            return
        embed = discord.Embed(
            title='Definitions',
            description=f'Definitions for the word "{word}"',
            color=0xFF0000,
        )


        item_dict = {
            "Noun": "",
            "Verb": "",
            "Adjective": "",
            "Adverb": "",
            "synonyms": "",
            "antonyms": ""
        }

        item_list = [
            'Noun', 'Verb', 'Adjective', 'Adverb'
        ]

        for item in item_list:
            if item in meaning:
                for item_meaning in meaning[item]:
                    if '(' in item_meaning or item_meaning.startswith('or'):
                        continue
                    item_dict[item] += item_meaning + "\n\n"
                item_dict[item] = item_dict[item].replace('(', '')
                embed.add_field(name=item, value=item_dict[item])

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="translate",
        description="Define a word",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="from",
                description="which language to translate from?",
                option_type=3,
                required=True
            ),
            create_option(
                name="to",
                description="which language to translate to?",
                option_type=3,
                required=True
            ),
            create_option(
                name="text",
                description="the text to translate",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption
    )
    async def translate(self, ctx: discord_slash.SlashContext, **kwargs):
        """Translate a string from a chosen language to a chosen language and relay it in an embed."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        origin = kwargs['from']
        destination = kwargs['to']
        await ctx.defer(hidden=ephemeral)
        translator = Translator(from_lang=origin, to_lang=destination)
        output = translator.translate(kwargs['text'])
        await ctx.send(embed=discord.Embed(title='Translation', description=output, color=0xFF0000))

    @cog_ext.cog_slash(
        name="wiki",
        description="Look something up on Wikipedia",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="query",
                description="what to look up?",
                option_type=3,
                required=True
            ),
            create_option(
                name="dansk",
                description="find results in danish",
                option_type=5,
                required=False
            )
        ] + functions.utils.privateOption
    )
    async def wiki(self, ctx: discord_slash.SlashContext, **kwargs):
        """Look something up on wikipedia and relay it in one or multiple embeds."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        await ctx.defer(hidden=ephemeral)
        if 'dansk' in kwargs and kwargs["dansk"] is True:
            wikipedia.set_lang('da')
        else:
            wikipedia.set_lang('en')
        output = wikipedia.summary(kwargs["query"])
        pagetitle = wikipedia.page(kwargs["query"]).title
        url = wikipedia.page(kwargs["query"]).url
        thumbnail = wikipedia.page(kwargs["query"]).images[0]
        if len(output) > 2048:
            num = 2048
            chunks = [output[i:i+num] for i in range(0, len(output), num)]
            for i in enumerate(chunks):
                title = pagetitle if i == 0 else '‌'
                embed = discord.Embed(title=title, description=chunks[i], color=0xFF0000, url=url)
                embed.set_thumbnail(url=thumbnail)
                await ctx.send(embed=embed, hidden=ephemeral)
        else:
            embed = discord.Embed(title=pagetitle, description=output, color=0xFF0000, url=url)
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed, hidden=ephemeral)



    @cog_ext.cog_slash(
        name="wolfram",
        description="Look something up on Wolfram Alpha",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="query",
                description="what to look up?",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption
    )
    async def wolfram(self, ctx: discord_slash.SlashContext, **kwargs):
        """Look something up on wolframaplha.com and relay it to the user through an embed."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        query = kwargs["query"]
        config = configparser.ConfigParser()
        config.read('cred.ini')
        app_id = config['config']['wolframID']
        client = wolframalpha.Client(app_id)
        await ctx.defer(hidden=ephemeral)
        response = client.query(query)
        try:
            output = next(response.results).text
            await ctx.send(embed=discord.Embed(title=f'Answer for query: {query}', description=output, color=0xFF0000))
        except StopIteration:
            await ctx.send(embed=discord.Embed(title=f'No results found for "{query}"', description='', color=0xFF0000))

    @cog_ext.cog_slash(
        name="google",
        description="Look something up on Google",
        guild_ids=functions.utils.servers,
        default_permission=True,
        permissions=functions.utils.slash_perms("banned"),
        options=[
            create_option(
                name="query",
                description="what to look up?",
                option_type=3,
                required=True
            )
        ] + functions.utils.privateOption
    )
    async def google(self, ctx: discord_slash.SlashContext, **kwargs):
        """Googles something and sends the first ten results to the user with buttons to cycle through the links."""
        ephemeral = functions.utils.ephemeral_check(**kwargs)
        query = kwargs["query"]
        await ctx.defer(hidden=ephemeral)
        i = 0
        results = list(search(query, tld='co.in', num=10, stop=10, pause=2))
        action_row = create_actionrow(
            create_button(style=ButtonStyle.green, label="Previous", custom_id="previousButton"),
            create_button(style=ButtonStyle.green, label="Next", custom_id="nextButton")
        )
        try:
            await ctx.send(results[0], hidden=ephemeral, components=[action_row])
        except IndexError:
            await ctx.send(embed=discord.Embed(title=f"No results found for '{query}'", color=0xFF0000))
            return

        while True:
            button_ctx: discord_slash.ComponentContext = await wait_for_component(self.bot, components=action_row)
            if button_ctx.custom_id == "previousButton":
                i -= 1
            else:
                i += 1

            await button_ctx.edit_origin(content=str(results[i]))


def setup(bot):
    """Adds the cog."""
    bot.add_cog(Lookup(bot))
