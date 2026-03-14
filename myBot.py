import os
import discord
from discord.ext import commands
from discord import Message
from discord.ext.commands.context import Context

from dotenv import load_dotenv
from utils.configuration import Terminal_Style

class MyBot(commands.Bot):
    MAIN_GUILD = 859442271908266034
    TEST_GUILD = 1347349188152791102

    COMMAND_CHANNELS =[866907725463289926,
                       893163728835579944,
                       859442273157644305,]
    def __init__(self):
        load_dotenv(dotenv_path='./config.env')
        super().__init__(command_prefix=commands.when_mentioned_or("nc!"),
                         case_insensitive=True,
                         intents=discord.Intents.all(),)
        self.loaded_cogs = set()
        self.token = os.getenv("TOKEN")

    # async def on_message(self, message: Message):
    #     if message.guild:
    #         if message.guild.id == MyBot.MAIN_GUILD:
    #             if message.channel.id not in MyBot.COMMAND_CHANNELS:
    #                 if not message.author.guild_permissions.administrator:
    #                     return

    #     await self.process_commands(message)

    async def on_message_edit(self, before, after):
        await self.process_commands(after)
        
    async def on_ready(self):
        print(f"Bot conectado como {self.user}")
        
    async def setup_hook(self):
        await self.load_extension(f'cogs.cogs.main')
        self.loaded_cogs.add("cogs")
        print("Setup finalizado")