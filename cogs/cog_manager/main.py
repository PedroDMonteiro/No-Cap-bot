import os

from discord.ext import commands
from discord.ext.commands.context import Context

from log import Log_Type
from utils import checks
from myBot import MyBot
from utils.cog import Cog

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Cog_Manager(bot))

class Cog_Cog_Manager(Cog, name = "Cog_Manager"):
    @commands.guild_only()
    @commands.group(name="cog",
                    aliases=["cogs"],
                    invoke_without_command=True)
    async def cogs(self, context: Context):
        if context.subcommand_passed == None:
            await context.send("Cogs carregados:\n")
            for cog in self.bot.loaded_cogs:
                await context.send(f"{cog}\n")

    @cogs.command(name="load",
                  aliases=["l"])
    @checks.is_developer()
    async def cogs_load(self, context: Context, cog_name: str):
        if cog_name in self.bot.loaded_cogs:
            await context.send(f"`{cog_name}` already loaded\n-# Use nc!cog unload or nc!cog reload")
            return
        
        if not (await self.load(cog_name)):
            await context.send(f"Erro ao carregar {cog_name }.")
            return
        
        await context.send(f"{cog_name} carregado.")

    async def load(self, cog_name: str) -> bool:
        for filename in os.listdir(f"./cogs/{cog_name}"):
            if filename.endswith(".py"):
                extension = f"cogs.{cog_name}.{filename[:-3]}"
                try:
                    await self.bot.load_extension(extension)
                    # self.bot.log.print(Log_Type.DEBUG,
                    #                    f"{cog_name}.{filename[:-3]} loaded")
                except Exception as err:
                    await self.bot.log.embed(type=Log_Type.ERROR,module=self,message=f"Error to load {extension}: {err}")
                    await self.unload(cog_name)
                    return False
        try:
            self.bot.loaded_cogs.add(cog_name)
            self.bot.log.print(Log_Type.DEBUG,
                               f"{cog_name} loaded")
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,module=self,message=f"Error to load {cog_name}: {err}")
            await self.unload(cog_name)
            return False
        
        return True

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
        try:
            await self.unload(cog_name)
            await context.send(f"{cog_name} descarregado.")
        except:
            ...

    async def unload(self, cog_name: str) -> bool:
        for filename in os.listdir(f"./cogs/{cog_name}"):
            try:
                if filename.endswith(".py"):
                    await self.bot.unload_extension(f"cogs.{cog_name}.{filename[:-3]}")
                    # self.bot.log.print(Log_Type.DEBUG,
                    #                    f"{cog_name}.{filename[:-3]} unloaded")
            except Exception as err:
                await self.bot.log.embed(type=Log_Type.ERROR,module=self,message=f"Error to unload {cog_name}: {err}")
                return False
        
        self.bot.loaded_cogs.discard(cog_name)

        self.bot.log.print(Log_Type.DEBUG,
                           f"{cog_name} unloaded")
        return True
        

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