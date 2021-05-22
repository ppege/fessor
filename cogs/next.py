import discord
from discord.ext import commands
import functions.utils
import datetime
from configs import options
from functions.school import schedule

class Next(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @functions.utils.banned()
    @commands.command()
    async def next(self, ctx):
        today = datetime.datetime.today().weekday()
        today = str(today)
        usedSchedule = "L"
        if today == "0":
          usedSchedule = schedule.monday
        elif today == "1":
          usedSchedule = schedule.tuesday
        elif today == "2":
          usedSchedule = schedule.wednesday
        elif today == "3":
          usedSchedule = schedule.thursday
        elif today == "4":
          usedSchedule = schedule.friday
        now = datetime.datetime.now()
        hours = 2
        hours_added = datetime.timedelta(hours = hours)
        newtime = now + hours_added
        currentTime = newtime.strftime("%H:%M")
        print(currentTime)
        currentTime = int(str(currentTime).replace(':', ''))
        nextClass = "There is no next class today."
        classNum = 0
        for i in range(0, 7):
          if currentTime > schedule.times[i]:
            classNum = i
          else:
            classNum = classNum
        try:
          nextClass = schedule.times[classNum + 1]
        except:
          nextClass = "Der er ingen timer din klovn"
        await ctx.send(nextClass)

def setup(bot):
    bot.add_cog(Next(bot))
