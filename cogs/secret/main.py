from discord import Message

import discord
from discord.ext import commands
from discord.ext.commands import Bot,Cog

from myBot import MyBot

async def setup(bot: Bot):
    await bot.add_cog(Cog_Secret(bot))

class Cog_Secret(Cog, name = "Secret"):
    def __init__(self, bot: MyBot):
        self.bot = bot

    async def cog_load(self):
        self.channel = await self.bot.fetch_channel(1356712387163586801)

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