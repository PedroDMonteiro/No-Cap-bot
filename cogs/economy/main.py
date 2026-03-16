import asyncio
import datetime
import random
import types

from discord import DMChannel, Embed, Emoji, File, Member,Message, Role, VoiceChannel, VoiceState

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
    if voice.channel is None:
        return False
    
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
        self.talking = {}

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

    def add_talking_prizes(self, member_id: int):
        if member_id not in self.talking:
            return
        
        now = int(datetime.datetime.now().timestamp()//1)
        seconds_talking = now - self.talking[member_id]

        # 15xp per 10 min
        xp = 15*(seconds_talking/(10*60))
        xp = int(xp//1)
        self.database.add_xp(identifier=member_id,points=xp)

        # 5 coins per hour
        coins = 5*(seconds_talking//(60*60))
        self.database.add_coins(identifier=member_id,coins=coins)

        self.talking.pop(member_id, 0)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if after.channel is None and before.channel is None:
            print("what??")
            return
        
        if before.channel is not None and after.channel is not None:
            if before.channel == after.channel:
                if talking(before) == talking(after):
                    #not related to talking
                    return

        now = int(datetime.datetime.now().timestamp()//1)
        
        if talking(before):
            self.add_talking_prizes(member_id=member.id)
            
            members_talking_before = [m for m in before.channel.members
                                      if (not m.bot) and talking(m.voice)]
            if len(members_talking_before) == 1:
                self.add_talking_prizes(member_id=members_talking_before[0].id)

        if talking(after):
            members_talking_after = [m for m in after.channel.members 
                                    if (not m.bot) and talking(m.voice)]
            if len(members_talking_after) >= 2:
                self.talking[member.id] = now

            if len(members_talking_after) == 2:
                other_id = members_talking_after[0].id
                if other_id == member.id:
                    other_id = members_talking_after[1].id
                    
                self.talking[other_id] = now

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