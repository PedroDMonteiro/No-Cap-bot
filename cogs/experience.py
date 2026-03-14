import datetime
from typing import Union
from discord import DMChannel, Embed, Emoji, File, Member, Message, Role, VoiceState
from discord import DMChannel, TextChannel, VoiceChannel
import discord
from discord.ext import commands, tasks
from discord.ext.commands.context import Context
from discord.ext.commands import Cog

import database.user as db

from myBot import MyBot

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Experience(bot))

class Cog_Experience(Cog, name = "Experience"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.in_cooldown = {}
        self.counting_xp = {}
    
    def allow_xp(channel) -> bool:
        if isinstance(channel,DMChannel):
            return False
        
        return True
    
    @tasks.loop(seconds=15)
    async def update_cooldown(self) -> None:
        now = datetime.datetime.now().timestamp()//1
        cooldown = self.in_cooldown.copy()
        for user in self.in_cooldown:
            if self.in_cooldown:
                pass

    @update_cooldown.before_loop
    async def before_update_bot(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        
        if not self.allow_xp(channel=message.channel):
            return

        id = message.author.id
        if id in self.in_cooldown:
            return
        
        len(message.content)
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.guild.id != 1347349188152791102:
            return

        if before.channel is None and after.channel is None:
            return
        
        elif before.channel is None and after.channel is not None:
            
            #check if channel is suitable for xp
            #adds id to counting_xp
            channel = after.channel
            await channel.send(f'{member.name} has joined voice channel: {channel.name}')
            # You can send a message to a specific text channel
            # text_channel = bot.get_channel(YOUR_TEXT_CHANNEL_ID)
            # await text_channel.send(f'{member.name} just entered {channel.name}!')

        # A user leaves a channel (before.channel is not None, after.channel is None)
        elif before.channel is not None and after.channel is None:
            # if id in countg_xp add total xp to the database
            channel = before.channel
            await channel.send(f'{member.name} has left voice channel: {channel.name}')
            # text_channel = bot.get_channel(YOUR_TEXT_CHANNEL_ID)
            # await text_channel.send(f'{member.name} just left {channel.name}.')

        # A user moves between channels
        elif before.channel is not None and after.channel is not None:
            if member.id in self.counting_xp:
                if not self.allow_xp(after.channel):
                    ...
                    #adds xp to database

            if self.allow_xp(after.channel):
                ...

            # check if new channel its suitable for xp
            #   if not 
            #       if id in countg_xp add total xp to the database
            #       if not in return
            #   if yes add id to counting_xp
            if before.channel != after.channel:
                await after.channel.send(f'{member.name} moved from {before.channel.name} to {after.channel.name}')

            if before.mute != after.mute:
                await after.channel.send("Mute mudou")
        print(member)
        print(f"{before.self_mute=} {before.self_deaf=}")
        print(f"{after.self_mute=} {after.self_deaf=}")

    @commands.group(invoke_without_command=True)
    async def xp(self, context: Context):
        if context.guild is None:
            return
        if context.guild.id != 1347349188152791102:
            return
        user = db.get(identifier=context.author)
        await context.reply(f"Você tem {user.xp} XP")

    @xp.command(name="add")
    async def xp_add(self, context: Context, member: Member| int, points: int):
        if context.guild is None:
            return
        if context.guild.id != 1347349188152791102:
            return
        user = db.add_xp(identifier=member,points=points)
        await context.reply(f"`{user.username}` agora tem {user.xp} XP")

    @xp.command(name="edit")
    async def xp_edit(self, context: Context, member: Member| int, points: int):
        if context.guild is None:
            return
        if context.guild.id != 1347349188152791102:
            return
        user = db.edit_xp(identifier=member,points=points)
        await context.reply(f"`{user.username}` agora tem {user.xp} XP")

    @xp.command(name="top",aliases=["rank"])
    async def balance_top(self, context: Context, member: Member| int, coins: int):
        if context.guild is None:
            return
        if context.guild.id != 1347349188152791102:
            return
        users = db.get_xp_rank()
        text = f"1° {users[0].username}\n"
        text = f"2° {users[1].username}\n"
        text = f"3° {users[2].username}\n"
        await context.reply(text)