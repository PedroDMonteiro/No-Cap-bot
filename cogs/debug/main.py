from discord import Member
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Bot,Cog

from myBot import MyBot
from utils import checks
from utils import utils

async def setup(bot: Bot):
    await bot.add_cog(Cog_Debug(bot))

class Cog_Debug(Cog, name= "Debug"):
    def __init__(self, bot: MyBot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__cog_name__} is up")

    @commands.command(name="teste")
    @checks.is_developer()
    async def teste(self, context: Context, cog_name: str, attribute_name: str) -> None:
        cog_instance = self.bot.get_cog(cog_name) # The name here is the class name

        if cog_instance:
            # Access the shared parameter
            param_value = getattr(cog_instance, attribute_name)
            await context.send(f"{cog_name}.{attribute_name}:")
            if utils.Utils.is_iterable(param_value):
                await context.send("[")
                for v in param_value:
                    await context.send(v)
                await context.send("]")
        else:
            await context.send(f"{cog_name} not found or not loaded.")
    
    @commands.command()
    async def nick(self, context: Context, member: Member = None):
        user = context.author
        if member:
            user = member
        await context.reply(f"{user.global_name=}")
        await context.reply(f"{user.display_name=}")
        await context.reply(f"{user.name=}")
        await context.reply(f"{user.nick=}")