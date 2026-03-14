import asyncio
import datetime
import random

from discord import DMChannel, Embed, Emoji, File, Member,Message, Role, VoiceState

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Cog

import database.user as db

from myBot import MyBot
from cogs.economy.sqls import Database as db
from utils import checks
from utils.erros.database import User_Not_Found

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Economy(bot))

def talking(voice: VoiceState) -> bool:
    if voice.mute:
        return False
    
    if voice.self_mute:
        return False
    
    if voice.deaf:
        return False
    
    if voice.self_deaf:
        return False
    
    return True

class Cog_Economy(Cog, name = "Economy"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.database = db()
        self.in_cooldown = set()
        self.chat_xp = [866894423164846110 , # chat geral
                        1376389786469662812, # midias
                        866907725463289926 , # comandos
                        866904119167942656 , # memes
                        ]
        self.call_xp = [859442274698264586]
        self.call_vips = [860330511787622400]

    async def cog_load(self):
        print(f"{self.__cog_name__} is up")

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        self.new_member(member)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if message.channel.id not in self.chat_xp:
            return
        
        member = message.author
        if member.id in self.in_cooldown:
            return
        
        self.in_cooldown.add(member.id)

        xp = random.randint(1,15)
        self.database.add_xp(identifier=member.id,points=xp)
        
        await asyncio.sleep(15)
        self.in_cooldown.remove(member.id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):

        if after.channel:
            #change channel or alter state in channel
            if before.channel:

                #change channel
                if before.channel.id != after.channel.id:
                    #stop talking
                    if talking(before) and not talking(after):
                        if member.id in self.call_xp:
                            # add xp
                            # and remove from xp
                            ...
                    elif not talking(before) and talking(after):
                        if len([m for m in before.channel.members 
                                if not m.bot and talking(m.voice)]) >= 2:
                            self.call_vips[member.id] = int(datetime.datetime.now().timestamp()//1)
        # return
        if before.channel:
            
            members = [m for m in before.channel.members 
                       if not m.bot and talking(m.voice)]
            if len(members) > 1:
                if before.mute or before.deaf:
                    return
                
        if before.channel is None and after.channel is None:
            #something wierd happened
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

    @commands.group(name="balance",
                    aliases=["bal","atm","saldo","coins","moedas","moeda"],
                    invoke_without_command=True)
    async def balance(self, context: Context, member: Member = None):
        if context.subcommand_passed == None:
            if member is None:
                member = context.author
            user = self.database.get(identifier=member)
            await context.reply(f"{member} tem {user.coins} {"dobrão" if user.coins == 1 else "dobrões"}")

    @balance.command(name="add")
    async def balance_add(self, context: Context, member: Member| int, coins: int):
        user = self.database.add_coins(identifier=member,coins=coins)
        await context.reply(f"`{user.username}` agora tem {user.coins} {"dobrão" if user.coins == 1 else "dobrões"}")

    @balance.command(name="edit")
    async def balance_edit(self, context: Context, member: Member| int, coins: int):
        user = self.database.edit_coins(identifier=member,coins=coins)
        await context.reply(f"`{user.username}` agora tem {user.coins} {"dobrão" if user.coins == 1 else "dobrões"}")

    @balance.command(name="top",aliases=["rank"])
    async def balance_top(self, context: Context):
        users = self.database.get_coins_rank()
        text = ""
        text += f"1° {users[0].username}\n"
        text += f"2° {users[1].username}\n"
        text += f"3° {users[2].username}\n"
        await context.reply(text)

    @commands.group(name="experience",
                    aliases=["xp","nivel","level",],
                    invoke_without_command=True)
    async def experience(self, context: Context, member: Member = None):
        if context.subcommand_passed == None:
            if member is None:
                member = context.author
            user = self.database.get(identifier=member)
            await context.reply(f"{member} tem {user.xp} xp")

    @experience.command(name="add")
    async def experience_add(self, context: Context, member: Member| int, coins: int):
        user = self.database.add_xp(identifier=member,coins=coins)
        await context.reply(f"`{user.username}` agora tem {user.xp} xp")

    @experience.command(name="edit")
    async def experience_edit(self, context: Context, member: Member| int, coins: int):
        user = self.database.edit_xp(identifier=member,coins=coins)
        await context.reply(f"`{user.username}` agora tem {user.xp} xp")

    @experience.command(name="top",aliases=["rank"])
    async def experience_top(self, context: Context):
        users = self.database.get_xp_rank()
        text = ""
        text += f"1° {users[0].username}\n"
        text += f"2° {users[1].username}\n"
        text += f"3° {users[2].username}\n"
        await context.reply(text)

    def new_member(self, member:Member):
        try:
            user = self.database.get(member.id)
        except Exception as err:
            if isinstance(err,User_Not_Found):
                self.database.new_member(member)
            else:
                raise(err)