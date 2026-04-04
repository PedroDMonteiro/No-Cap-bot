import os
import discord
from discord.ext import commands

from dotenv import load_dotenv
from log import Log, Log_Type

class MyBot(commands.Bot):
    def __init__(self,
                 guild: int,
                 adm_roles:list[int] = [],
                 commands_channels:list[int] = [],
                 ):
        load_dotenv(dotenv_path='./config.env')
        super().__init__(command_prefix=commands.when_mentioned_or("nc!"),
                         case_insensitive=True,
                         intents=discord.Intents.all(),)
        self.guild_id = guild
        self.adm_roles = adm_roles
        self.commands_channels = commands_channels
        self.loaded_cogs = set()
        self.token = os.getenv("TOKEN")
        self.add_check(self.check)

    async def check(self, context: commands.Context):
        if context.guild:
            if context.author.guild_permissions.administrator:
                return True
            
            roles = [role.id for role in context.author.roles]
            for adm_role in self.adm_roles:
                if adm_role in roles:
                    return True
                
            if context.channel.id in self.commands_channels:
                return True
            
        return False

    async def on_message_edit(self, before, after):
        await self.process_commands(after)

    async def on_ready(self):
        print(f"Bot conectado como {self.user}")

    async def setup_hook(self):
        self.guild = await self.fetch_guild(self.guild_id)
        self.log = Log(default=1485802065509879948,
                       error=1485800424060489851,
                       moderation=873198241242578955,
                       call=968661076579344535,
                       guild=968662877605093386,
                       debug=1485801764623089734,)
        await self.log.setup(self)
        
        await self.load_initial_cogs()

        self.log.print(type=Log_Type.DEBUG,
                       module="setup_hook",
                       message="Setup finalizado")

    async def load_initial_cogs(self, ):
        for cog_name in os.listdir("./cogs"):
            if cog_name.count(".") == 0:
                if cog_name != "__pycache__":
                    await self.load_cog(cog_name)

        await self.log.embed(type=Log_Type.DEBUG,
                             module="Cog loader",
                             message="All avaiable cogs loaded")

    async def load_cog(self, cog_name: str):
        for filename in os.listdir(f"./cogs/{cog_name}"):
            try:
                if filename.endswith(".py"):
                    await self.load_extension(f"cogs.{cog_name}.{filename[:-3]}")
                    self.log.print(type=Log_Type.DEBUG,
                                   module="Cog loader",
                                   message=f'{cog_name}.{filename[:-3]} loaded')
            except Exception as err:
                await self.log.embed(type=Log_Type.ERROR,
                                         module="Cog Loader",
                                         message=f"Error to load {cog_name}: {err}")
                await self.unload_cog(cog_name)
                return
        try:
            self.loaded_cogs.add(cog_name)
            self.log.print(type=Log_Type.DEBUG,
                               module="Cog Loader",
                               message=f"{cog_name} loaded")
        except Exception as err:
            await self.log.embed(type=Log_Type.ERROR,
                                     module="Cog Loader",
                                     message=f"Error to load {cog_name}: {err}")
            await self.unload_cog(cog_name)

    async def unload_cog(self, cog_name: str):
        try:
            for filename in os.listdir(f"./cogs/{cog_name}"):
                try:
                    if filename.endswith(".py"):
                        await self.unload_extension(f"cogs.{cog_name}.{filename[:-3]}")
                        self.log.print(type=Log_Type.DEBUG,
                                       module="Cog loader",
                                       message=f'{cog_name}.{filename[:-3]} unloaded')
                except Exception as e:
                    self.log.embed(type=Log_Type.ERROR,
                                   module="Cog loader",
                                   message=f"Error to unload cogs.{cog_name}.{filename[:-3]}: {e}")
        except:
            ...
        try:
            self.loaded_cogs.remove(cog_name)
        except:
            ...

        self.log.embed(type=Log_Type.DEBUG,
                       module="Cog loader",
                       message=f"Cog {cog_name} unloaded: {e}")