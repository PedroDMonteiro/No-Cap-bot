import asyncio
import datetime

from discord import Message, User
from discord.ext import commands,tasks
from discord.ext.commands import Cog


from myBot import MyBot
from cogs.bump.sqls import Database as db

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Bump(bot))

class Cog_Bump(Cog, name = "Bump"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.last_bumped = int(datetime.datetime.now().timestamp()//1) - 2*60*60 + 50
        self.bump_bot = 302050872383242240
        self.database = db()
        
    async def cog_load(self):
        862204731896365086
        # self.channel = await self.bot.fetch_channel(862204731896365086)
        self.channel = await self.bot.fetch_channel(978480902093033512)
        print(f"{self.__cog_name__} is up")
        self.reminder.start()

    @tasks.loop(hours=1)
    async def reminder(self) -> None:
        now = int(datetime.datetime.now().timestamp()//1)

        if now >= self.last_bumped + 2*60*60:
            await self.channel.send("Dê bump e ganhe 10 NoCoins\n-# <@&945038105432424449>")

    @reminder.before_loop
    async def before_update_bot(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == self.bump_bot:
            if len(message.embeds) > 0:
                if message.embeds[0].description.startswith("Bump done!"):
                    await self.bumped(user=message.interaction_metadata.user)

    async def bumped(self, user: User):
        await self.channel.send(f"{user} obg pelo bump <:02_Heart2_NC:890999231840665650>")
        self.last_bumped = int(datetime.datetime.now().timestamp()//1)
        self.database.bumped(user_id=user.id)

        await asyncio.sleep(2*60*60)
        await self.reminder()