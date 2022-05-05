"""Changes the status every once in a while"""
from glob import glob
import discord
from discord.ext import tasks, commands
from pygount import ProjectSummary, SourceAnalysis

class Status(commands.Cog):
    """The status cog"""
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(seconds=600)
    async def change_status(self):
        """Changes the bot status"""
        print(self.index)
        self.index += 1

    @change_status.before_loop
    async def before_change_status(self):
        """This will run before the loop starts"""
        await self.bot.wait_until_ready()
        project_summary = ProjectSummary()
        source_paths = glob("**/*.py", recursive=True)
        for source_path in source_paths:
            source_analysis = SourceAnalysis.from_file(source_path, "pygount")
            project_summary.add(source_analysis)
        await self.bot.change_presence(activity=discord.Game(name=f"{project_summary.total_line_count} lines of code"))

def setup(bot):
    """Adds the cog."""
    # bot.add_cog(Status(bot))
    pass