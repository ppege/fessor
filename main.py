import discord
import os
import datetime
from threading import Timer
import pytz
import discord.ext.commands
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
import asyncio
import file
from school import schedule
print('importing lektiescanner')
from school.lektiescanner import lektiescan
print('finished importing lektiescanner')

lektiescan()
print(lektiescanner.beskrivelse[0])