from discord.ext import tasks
from discord.ext.commands import Cog as Cog_dc

from log import Log_Type
from myBot import MyBot

class Cog(Cog_dc):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.bot.cog_count += 1
        self.id = self.bot.cog_count

    async def cog_load(self):
            self.bot.log.print(Log_Type.DEBUG,
                            f"{self.__cog_name__}_{self.id:03} Up")

    async def cog_unload(self):
        for task in self.__dict__.values():
            if isinstance(task, tasks.Loop) and task.is_running():
                task.cancel()
                self.bot.log.print(Log_Type.DEBUG,f"task: {task._name} canceled")
        
        self.bot.log.print(Log_Type.DEBUG,
                           f"{self.__cog_name__}_{self.id:03} Down")