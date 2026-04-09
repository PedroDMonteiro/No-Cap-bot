import asyncio
import datetime

from discord import Member, Message
from discord.ext import commands,tasks

from log import Log_Type
from myBot import MyBot
from cogs.bump.sqls import Database as db
from utils.cog import Cog

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Bump(bot))

class Cog_Bump(Cog, name = "Bump"):
    async def cog_load(self):
        self.bump_bot = 302050872383242240
        self.last_bumped = int(datetime.datetime.now().timestamp()//1) - 2*60*60 + 50
        self.database = db()
        self.channel = await self.bot.fetch_channel(978480902093033512)
        self.reminder.start()
        await super().cog_load()

    @tasks.loop(hours=1)
    async def reminder(self) -> None:
        now = int(datetime.datetime.now().timestamp()//1)

        if now >= self.last_bumped + 2*60*60:
            await self.channel.send("Dê bump e ganhe 10 NoCoins\n-# <@&945038105432424449>\n-# <@&865415575902355487>")

    @reminder.before_loop
    async def before_update_bot(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == self.bump_bot:
            if len(message.embeds) > 0:
                if message.embeds[0].description.startswith("Bump done!"):
                    await self.bumped(member=message.interaction_metadata.user)

    async def bumped(self, member: Member):
        await self.channel.send(f"{member} obg pelo bump <:02_Heart2_NC:890999231840665650>")
        self.last_bumped = int(datetime.datetime.now().timestamp()//1)
        self.database.bumped(member_id=member.id)

        await asyncio.sleep(2*60*60)
        await self.reminder()