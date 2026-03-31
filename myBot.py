import os
import discord
from discord.ext import commands

from dotenv import load_dotenv
from log import Log

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
        self.log = Log(self,
                       default=1485802065509879948,
                       error=1485800424060489851,
                       moderation=873198241242578955,
                       call=968661076579344535,
                       guild=968662877605093386,
                       debug=1485801764623089734,)

        print(f"Bot conectado como {self.user}")

    async def setup_hook(self):
        await self.load_extension(f'cogs.cogs.main')
        self.loaded_cogs.add("cogs")
        print("Setup finalizado")