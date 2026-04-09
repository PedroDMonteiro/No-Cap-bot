from discord import Message

import discord
from discord.ext import commands

from myBot import MyBot
from utils.cog import Cog

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Secret(bot))

class Cog_Secret(Cog, name = "Secret"):
    async def cog_load(self):
        self.channel = await self.bot.fetch_channel(1356712387163586801)
        await super().cog_load()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id != self.bot.user.id:
            if isinstance(message.channel, discord.channel.DMChannel):
                msg = f"## {message.author} Send \n-# ID:{message.author.id}\n" + message.content
                await self.channel.send(msg, files=[
                    await attch.to_file() for attch in message.attachments])

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.id != self.bot.user.id:
            if isinstance(after.channel, discord.channel.DMChannel):
                after.content = f"## {after.author} Send \n-# ID:{after.author.id}\n" + after.content
                await self.channel.send(after.content, files=[
                    await attch.to_file() for attch in after.attachments])