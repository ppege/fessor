import discord
from discord.ext import commands
import functions.utils
from PyDictionary import PyDictionary
from translate import Translator
import wikipedia
import wolframalpha
import configparser

class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def define(self, ctx, word):
        message = await ctx.send(embed=discord.Embed(title=f'Checking definitions for the word "{word}"...', description=''))
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

        for i in range(len(synonym)):
            if '(' in synonym[i] or synonym[i].startswith('or'):
                continue
            synonyms = synonyms + synonym[i] + ", "
        synonyms = synonyms.replace('(', '')[:-2]
        embed.add_field(name='Synonyms', value=synonyms)

        for i in range(len(antonym)):
            if '(' in antonym[i] or antonym[i].startswith('or'):
                continue
            antonyms = antonyms + antonym[i] + ", "
        antonyms = antonyms.replace('(', '')[:-2]
        embed.add_field(name='Antonyms', value=antonyms)

        await message.edit(embed=embed)

    @functions.utils.banned()
    @commands.command()
    async def translate(self, ctx, dest, *, words):
        dest = dest.partition('-')
        origin = dest[0]
        destination = dest[2]
        translator = Translator(from_lang=origin, to_lang=destination)
        output = translator.translate(words)
        await ctx.send(embed=discord.Embed(title=f'Translation', description=output, color=0xFF0000))

    @functions.utils.banned()
    @commands.command()
    async def wiki(self, ctx, *, query):
        if query.split(' ')[0] == "--dansk":
            query = query.replace('--dansk ', '')
            wikipedia.set_lang('da')
        else:
            wikipedia.set_lang('en')
        output = wikipedia.summary(query)
        pagetitle = wikipedia.page(query).title
        url = wikipedia.page(query).url
        thumbnail = wikipedia.page(query).images[0]
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
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=title, description=output, color=0xFF0000, url=url)
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed)

    @functions.utils.banned()
    @commands.command()
    async def wolfram(self, ctx, *, query):
        config = configparser.ConfigParser()
        config.read('cred.ini')
        appID = config['config']['wolframID']
        client = wolframalpha.Client(appID)
        message = await ctx.send(embed=discord.Embed(title=f'Searching for "{query}"...', description='This might take a while.'))
        response = client.query(query)
        try:
            output = next(response.results).text
            await message.edit(embed=discord.Embed(title=f'Answer for query: {query}', description=output, color=0xFF0000))
        except:
            await message.edit(embed=discord.Embed(title=f'No results found for "{query}"', description='', color=0xFF0000))

def setup(bot):
    bot.add_cog(Lookup(bot))
