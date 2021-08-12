import discord
from discord.ext import commands
import functions.utils
from PyDictionary import PyDictionary
from translate import Translator
import wikipedia
import wolframalpha
import configparser
from googlesearch import search
import discord_slash
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component, create_button, create_actionrow
from discord_slash.model import ButtonStyle


class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @cog_ext.cog_slash(name="define",
                        description="Define a word",
                        guild_ids=functions.utils.servers,
                        options=[
                            create_option(
                                name="word",
                                description="which word to define?",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ])
    async def define(self, ctx: discord_slash.SlashContext, word, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.defer(hidden=ephemeral)
        dict = PyDictionary()
        meaning = dict.meaning(word)
        synonym = dict.synonym(word)
        antonym = dict.antonym(word)
        print(meaning)
        embed = discord.Embed(title=f'Definitions for {word}', description=f'Definitions, synonyms and antonyms for the word "{word}"', color=0xFF0000)
        nouns = ""
        verbs = ""
        adjectives = ""
        adverbs = ""
        synonyms = ""
        antonyms = ""

        if 'Noun' in meaning:
            for i in range(len(meaning['Noun'])):
                if '(' in meaning['Noun'][i] or meaning['Noun'][i].startswith('or'):
                    continue
                nouns = nouns + meaning['Noun'][i] + "\n\n"
            nouns = nouns.replace('(', '')
            embed.add_field(name='Noun', value=nouns)

        if 'Verb' in meaning:
            for i in range(len(meaning['Verb'])):
                if '(' in meaning['Verb'][i] or meaning['Verb'][i].startswith('or'):
                    continue
                verbs = verbs + meaning['Verb'][i] + "\n\n"
            verbs = verbs.replace('(', '')
            embed.add_field(name='Verb', value=verbs)

        if 'Adjective' in meaning:
            for i in range(len(meaning['Adjective'])):
                if '(' in meaning['Adjective'][i] or meaning['Adjective'][i].startswith('or'):
                    continue
                adjectives = adjectives + meaning['Adjective'][i] + "\n\n"
            adjectives = adjectives.replace('(', '')
            embed.add_field(name='Adjective', value=adjectives)

        if 'Adverb' in meaning:
            for i in range(len(meaning['Adverb'])):
                if '(' in meaning['Adverb'][i] or meaning['Adverb'][i].startswith('or'):
                    continue
                adverbs = adverbs + meaning['Adverb'][i] + "\n\n"
            adverbs = adverbs.replace('(', '')
            embed.add_field(name='Adverb', value=adverbs)

        if synonym != None:
            for i in range(len(synonym)):
                if '(' in synonym[i] or synonym[i].startswith('or'):
                    continue
                synonyms = synonyms + synonym[i] + ", "
            synonyms = synonyms.replace('(', '')[:-2]
            embed.add_field(name='Synonyms', value=synonyms)

        if antonym != None:
            for i in range(len(antonym)):
                if '(' in antonym[i] or antonym[i].startswith('or'):
                    continue
                antonyms = antonyms + antonym[i] + ", "
            antonyms = antonyms.replace('(', '')[:-2]
            embed.add_field(name='Antonyms', value=antonyms)

        await ctx.send(embed=embed)

    @functions.utils.banned()
    @cog_ext.cog_slash(name="translate",
                        description="Define a word",
                        guild_ids=functions.utils.servers,
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
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )

    async def translate(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        origin = kwargs['from']
        destination = kwargs['to']
        await ctx.defer(hidden=ephemeral)
        translator = Translator(from_lang=origin, to_lang=destination)
        output = translator.translate(kwargs['text'])
        await ctx.send(embed=discord.Embed(title=f'Translation', description=output, color=0xFF0000))

    @functions.utils.banned()
    @cog_ext.cog_slash(name="wiki",
                        description="Look something up on Wikipedia",
                        guild_ids=functions.utils.servers,
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
                            ),
                            create_option(
                                name="private",
                                description="send the message privately?",
                                option_type=5,
                                required=False
                            )
                        ]
                    )
    async def wiki(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        await ctx.defer(hidden=ephemeral)
        if 'dansk' in kwargs:
            if kwargs["dansk"] == True:
                wikipedia.set_lang('da')
            else:
                wikipedia.set_lang('en')
        else:
            wikipedia.set_lang('en')
        output = wikipedia.summary(kwargs["query"])
        pagetitle = wikipedia.page(kwargs["query"]).title
        url = wikipedia.page(kwargs["query"]).url
        thumbnail = wikipedia.page(kwargs["query"]).images[0]
        if len(output) > 2048:
            n = 2048
            chunks = [output[i:i+n] for i in range(0, len(output), n)]
            for i in range(len(chunks)):
                if i == 0:
                    title = pagetitle
                else:
                    title = '‌'
                embed = discord.Embed(title=title, description=chunks[i], color=0xFF0000, url=url)
                embed.set_thumbnail(url=thumbnail)
                await ctx.send(embed=embed, hidden=ephemeral)
        else:
            embed = discord.Embed(title=pagetitle, description=output, color=0xFF0000, url=url)
            embed.set_thumbnail(url=thumbnail)
            await message.edit(embed=embed, hidden=ephemeral)



    @functions.utils.banned()
    @cog_ext.cog_slash(name="wolfram",
                        description="Look something up on Wolfram Alpha",
                        guild_ids=functions.utils.servers,
                        options=[
                            create_option(
                                name="query",
                                description="what to look up?",
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
    async def wolfram(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        query = kwargs["query"]
        config = configparser.ConfigParser()
        config.read('cred.ini')
        appID = config['config']['wolframID']
        client = wolframalpha.Client(appID)
        await ctx.defer(hidden=ephemeral)
        response = client.query(query)
        try:
            output = next(response.results).text
            await ctx.send(embed=discord.Embed(title=f'Answer for query: {query}', description=output, color=0xFF0000))
        except:
            await ctx.send(embed=discord.Embed(title=f'No results found for "{query}"', description='', color=0xFF0000))

    @functions.utils.banned()
    @cog_ext.cog_slash(name="google",
                        description="Look something up on Google",
                        guild_ids=functions.utils.servers,
                        options=[
                            create_option(
                                name="query",
                                description="what to look up?",
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
    async def google(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        query = kwargs["query"]
        await ctx.defer(hidden=ephemeral)
        i = 0
        results = []
        reaction = None
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):
            results.append(j)

        action_row = create_actionrow(
            create_button(style=ButtonStyle.green, label="Previous", custom_id="previousButton"),
            create_button(style=ButtonStyle.green, label="Next", custom_id="nextButton")
        )

        await ctx.send(results[0], hidden=ephemeral, components=[action_row])

        while True:
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row)
            if button_ctx.custom_id == "previousButton":
                i = i - 1
                await button_ctx.edit_origin(content=str(results[i]))
            else:
                i = i + 1
                await button_ctx.edit_origin(content=str(results[i]))
            #await button_ctx.edit_origin(content=f"{button_ctx.custom_id}")
            #if str(reaction) == '➡️':
            #    i = i + 1
            #    await message.edit(content=str(results[i]))
            #elif str(reaction) == '⬅️':
            #    i = i - 1
            #    await message.edit(content=str(results[i]))

            #try:
            #    reaction, user = await self.bot.wait_for('reaction_add', timeout = 60.0, check = check)
            #except:
            #    break


def setup(bot):
    bot.add_cog(Lookup(bot))
