from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Bot,Cog

from myBot import MyBot
from cogs.database.sqls import Database as db
from utils import checks
from utils.erros.database import Table_Not_Found

async def setup(bot: Bot):
    await bot.add_cog(Cog_Debug(bot))

class Cog_Debug(Cog, name= "Debug"):
    def __init__(self, bot: MyBot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__cog_name__} is up")

    @commands.command(name="teste")
    @checks.is_developer()
    async def teste(self, context: Context, *args) -> None:
        cog_a_instance = self.bot.get_cog("Economy") # The name here is the class name

        if cog_a_instance:
            # Access the shared parameter
            param_value = cog_a_instance.talking
            await context.send(f"Pessoas contando xp em call:\n {[f"<@{id}>" for id in param_value]}")
        else:
            await context.send("CogA not found or not loaded.")
    