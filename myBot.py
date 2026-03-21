import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

class MyBot(commands.Bot):
    MAIN_GUILD = 859442271908266034
    TEST_GUILD = 1347349188152791102
    COMMAND_CHANNELS = [866907725463289926] # comandos

    ADM_ROLES = [867875024193978368, # ADM
                 861808601421185034, # VICE
                 933768048865853501, # DONA
                 868847569336426546, # DONO
                 ]

    def __init__(self):
        load_dotenv(dotenv_path='./config.env')
        super().__init__(command_prefix=commands.when_mentioned_or("nc!"),
                         case_insensitive=True,
                         intents=discord.Intents.all(),)
        self.loaded_cogs = set()
        self.token = os.getenv("TOKEN")
        self.log = Log(self)
        self.add_check(self.check)

    async def check(self, context: commands.Context):
        print(f"{context.author}:{context.command.name}")
        if context.guild:
            if context.author.guild_permissions.administrator:
                return True
            
            roles = [role.id for role in context.author.roles]
            for adm_role in self.ADM_ROLES:
                if adm_role in roles:
                    return True
                
            if context.channel.id in self.COMMAND_CHANNELS:
                return True
            
        return False

    async def on_message_edit(self, before, after):
        await self.process_commands(after)

    async def on_ready(self):
        self.log_channel = await self.fetch_channel(862204731896365086)
        print(f"Bot conectado como {self.user}")

    async def setup_hook(self):
        await self.load_extension(f'cogs.cogs.main')
        self.loaded_cogs.add("cogs")
        print("Setup finalizado")