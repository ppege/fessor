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
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import wait_for_component, create_button, create_actionrow
from discord_slash.model import ButtonStyle


class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="define",
                        description="Define a word",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
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
    async def define(self, ctx: discord_slash.SlashContext, **kwargs):
        ephemeral = functions.utils.eCheck(**kwargs)
        word = kwargs["word"]
        await ctx.defer(hidden=ephemeral)
        dict = PyDictionary()
        meaning = dict.meaning(word)
        if meaning is None:
            await ctx.send(embed=discord.Embed(title=f"No definition found for {word}", color=0xFF0000))
            return
        embed = discord.Embed(
            title='Definitions',
            description=f'Definitions for the word "{word}"',
            color=0xFF0000,
        )


        itemDict={
            "Noun": "",
            "Verb": "",
            "Adjective": "",
            "Adverb": "",
            "synonyms": "",
            "antonyms": ""
        }

        itemList=[
            'Noun', 'Verb', 'Adjective', 'Adverb'
        ]

        for item in itemList:
            if item in meaning:
                for itemMeaning in meaning[item]:
                    if '(' in itemMeaning or itemMeaning.startswith('or'):
                        continue
                    itemDict[item] += itemMeaning + "\n\n"
                itemDict[item] = itemDict[item].replace('(', '')
                embed.add_field(name=item, value=itemDict[item])

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="translate",
                        description="Define a word",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
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
        await ctx.send(embed=discord.Embed(title='Translation', description=output, color=0xFF0000))

    @cog_ext.cog_slash(name="wiki",
                        description="Look something up on Wikipedia",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
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
        if 'dansk' in kwargs and kwargs["dansk"] == True:
            wikipedia.set_lang('da')
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
                title = pagetitle if i == 0 else '‌'
                embed = discord.Embed(title=title, description=chunks[i], color=0xFF0000, url=url)
                embed.set_thumbnail(url=thumbnail)
                await ctx.send(embed=embed, hidden=ephemeral)
        else:
            embed = discord.Embed(title=pagetitle, description=output, color=0xFF0000, url=url)
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed, hidden=ephemeral)



    @cog_ext.cog_slash(name="wolfram",
                        description="Look something up on Wolfram Alpha",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
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

    @cog_ext.cog_slash(name="google",
                        description="Look something up on Google",
                        guild_ids=functions.utils.servers,
                        default_permission=True,
                        permissions=functions.utils.slPerms("banned"),
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
        reaction = None
        results = [j for j in search(query, tld="co.in", num=10, stop=10, pause=2)]
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
