"""Adds several commands that help users look things up."""
from typing import Union
import string
import json
import configparser
import discord
from discord.ext import commands
from PyDictionary import PyDictionary
from translate import Translator
from langdetect import detect
import wikipedia
import wolframalpha
from googlesearch import search
import discord_slash
from discord_slash import cog_ext
from discord_slash.context import ComponentContext, MenuContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import wait_for_component, create_button, create_actionrow, create_select, create_select_option
from discord_slash.model import ButtonStyle, ContextMenuType
import functions.utils # pylint: disable=import-error


class Lookup(commands.Cog):
    """Lookup cog."""
    def __init__(self, bot):
        self.bot = bot
        with open("configs/countries.json", "r") as file:
            langs = json.load(file)
        self.langs = langs
        with open("configs/country_names.json", "r") as file:
            countries = json.load(file)
        self.countries = countries

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
    @staticmethod
    async def define(ctx: discord_slash.SlashContext, **kwargs):
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

    async def make_translation(self, **kwargs):
        """Make the translation"""
        ctx = kwargs['ctx']
        from_lang = kwargs['from_lang']
        sentence = kwargs['sentence'].capitalize()
        edit = kwargs['edit']
        to_lang = kwargs['to_lang'].capitalize() if 'to_lang' in kwargs else 'English'
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        output = translator.translate(sentence)
        if sentence == output:
            return "fail"
        if "LANGPAIR=EN|IT" in output:
            translator = Translator(from_lang=list(self.langs.keys())[list(self.langs.values()).index(from_lang)], to_lang=to_lang)
            output = translator.translate(sentence)
        embed=discord.Embed(title='Translation', color=0xFF0000)
        if edit:
            embed.add_field(name=f'Original text | {from_lang}', value=sentence)
        else:
            try:
                embed.add_field(name=f'Original text | {self.langs[from_lang]}', value=sentence)
            except KeyError:
                embed.add_field(name=f'Original text | {from_lang}', value=sentence)
        embed.add_field(name=f'Translation | {to_lang}', value=output, inline=False)
        await ctx.send(embed=embed) if not edit else await ctx.edit_origin(embed=embed, components=[])
        return "success"

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
        from_lang = kwargs['from']
        to_lang = kwargs['to']
        await ctx.defer(hidden=ephemeral)
        output = await self.make_translation(ctx=ctx, from_lang=from_lang.capitalize(), to_lang=to_lang, sentence=kwargs['text'], edit=False)
        if output == "fail":
            await ctx.send(
                embed=discord.Embed(
                    title="Failure",
                    description="Translation is the same as the original - maybe the language isn't set correctly."
                )
            )

    @cog_ext.cog_context_menu(
        target=ContextMenuType.MESSAGE,
        name="Translate to English",
        guild_ids=functions.utils.servers
    )
    async def translate_to_english(self, ctx: Union[ComponentContext, MenuContext]):
        """Translates the selected message's contents to english."""
        sentence = ctx.target_message.content
        sentence_language = self.langs[detect(sentence)]
        output = await self.make_translation(ctx=ctx, from_lang=sentence_language, sentence=sentence, edit=False)
        if output == "fail":
            lang_dict = {}
            for value in self.langs.values():
                try:
                    lang_dict[value[0]].append(value)
                except:
                    lang_dict[value[0]] = [value]
            action_row = create_actionrow(
                create_select(
                    [
                        create_select_option(letter, value=letter) for letter in string.ascii_uppercase[:-1]
                    ]
                )
            )

            await ctx.send(
                embed=discord.Embed(
                    title="Could not detect language.",
                    description="Please select the first letter of the origin language manually below."
                ),
                components=[action_row]
            )
            select_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row)
            action_row = create_actionrow(
                create_select(
                    [
                        create_select_option(lang, value=lang) for lang in lang_dict[select_ctx.selected_options[0]]
                    ]
                )
            )
            await select_ctx.edit_origin(embed=discord.Embed(
                    title="Could not detect language.",
                    description="Please select the origin language manually below."
                ),
                components=[action_row])
            select_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row)
            output = await self.make_translation(ctx=select_ctx, from_lang=select_ctx.selected_options[0], sentence=sentence, edit=True)

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
    @staticmethod
    async def wiki(ctx: discord_slash.SlashContext, **kwargs):
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
    @staticmethod
    async def wolfram(ctx: discord_slash.SlashContext, **kwargs):
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
