import os

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Cog

from log import Log_Type
from utils import checks
from myBot import MyBot
from utils.configuration import Terminal_Style

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Cogs(bot))

class Cog_Cogs(Cog, name = "Cogs"):
    def __init__(self, bot: MyBot):
        self.bot = bot

    async def cog_load(self):
        print(f"{self.__cog_name__} is up!")
        ...

    async def cog_uload(self):
        pass

    @commands.guild_only()
    @commands.group(name="cog",
                    aliases=["cogs"],
                    invoke_without_command=True)
    async def cogs(self, context: Context):
        if context.subcommand_passed == None:
            await context.send("Cogs carregados:\n")
            for c in self.bot.loaded_cogs:
                await context.send(f"{c}\n")

    @cogs.command(name="load",
                  aliases=["l"])
    @checks.is_developer()
    async def cogs_load(self, context: Context, cog_name: str):
        if cog_name in self.bot.loaded_cogs:
            await context.send(f"`{cog_name}` already loaded\n-# Use nc!cog unload or nc!cog reload")
            return
        
        await self.load(cog_name)
        await context.send(f"{cog_name} carregado.")

    async def load(self, cog_name: str):
        for filename in os.listdir(f"./cogs/{cog_name}"):
            try:
                if filename.endswith(".py"):
                    await self.bot.load_extension(f"cogs.{cog_name}.{filename[:-3]}")
                    print(f"{cog_name}.{filename[:-3]} loaded{Terminal_Style.RESET}")
            except Exception as err:
                await self.bot.log.embed(type=Log_Type.ERROR,module="Cog Loader",message=f"Error to load {cog_name}: {err}")
                await self.unload(cog_name)
                return
        try:
            self.bot.loaded_cogs.add(cog_name)
            self.bot.log.print(type=Log_Type.DEBUG,module="Cog Loader",message=f"{cog_name} loaded")
            print(f'{Terminal_Style.GREEN}Cog {cog_name} loaded{Terminal_Style.RESET}')
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,module="Loader",message=f"Error to load {cog_name}: {err}")
            print(f'{Terminal_Style.RED}Error to load {cog_name}: {err}{Terminal_Style.RESET}')
            await self.unload(cog_name)

    @cogs.command(name="unload",
                  aliases=["u"])
    @checks.is_developer()
    async def cogs_unload(self, context: Context, cog_name: str):
        cog_name = cog_name.lower()
        if cog_name == "cogs":
            await context.send(f"If wanna change something in cogs module restart me")
            return

        if cog_name not in self.bot.loaded_cogs:
            await context.send(f"`{cog_name}` not loaded\n-# Use nc!cog load or nc!cog reload")
            return
        
        await self.unload(cog_name)
        await context.send(f"{cog_name} descarregado.")

    async def unload(self, cog_name: str):
        try:
            for filename in os.listdir(f"./cogs/{cog_name}"):
                try:
                    if filename.endswith(".py"):
                        await self.bot.unload_extension(f"cogs.{cog_name}.{filename[:-3]}")
                        print(f'{cog_name}.{filename[:-3]} unloaded{Terminal_Style.RESET}')
                except Exception as e:
                    print(f'{Terminal_Style.RED}Error to unload {cog_name}: {e}{Terminal_Style.RESET}')
        except:
            ...
        try:
            self.bot.loaded_cogs.remove(cog_name)
        except:
            ...
        print(f'{Terminal_Style.GREEN}Cog {cog_name} unloaded{Terminal_Style.RESET}')

    @cogs.command(name="reload",
                  aliases=["r"])
    @checks.is_developer()
    async def cogs_reload(self, context: Context, cog_name: str):
        cog_name = cog_name.lower()
        if cog_name == "cogs":
            await context.send(f"If wanna change something in cogs module restart me")
            return

        if cog_name not in self.bot.loaded_cogs:
            await context.send(f"`{cog_name}` not loaded\n-# Use nc!cog load")
            return

        await self.unload(cog_name)
        await self.load(cog_name)
        await context.send(f"{cog_name} recarregado.")