import asyncio
import datetime

from discord import Message

from discord.ext import commands,tasks
from discord.ext.commands import Bot,Cog

from myBot import MyBot

async def setup(bot: Bot):
    await bot.add_cog(Cog_VIPs(bot))

class Cog_VIPs(Cog, name = "VIPs"):
    def __init__(self, bot: MyBot):
        self.bot = bot