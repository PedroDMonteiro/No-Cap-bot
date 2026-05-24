import asyncio
import datetime
import random

from discord import Member, Message, VoiceState

from discord.ext import commands
from discord.ext.commands.context import Context

from myBot import MyBot
from cogs.economy.sqls import Database as db
from cogs.economy.models.user import User as md_User
from log import Log_Type
from utils import checks
from utils.erros.database import User_Not_Found
from utils.utils import Utils
from utils.cog import Cog

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
    async def cog_load(self):
        self.database = db()
        self.in_cooldown = set()
        self.chat_xp = [866894423164846110 , # chat geral
                        1376389786469662812, # midias
                        866907725463289926 , # comandos
                        866904119167942656 , # memes
                        ]
        self.call_xp_category = [859442274698264586, # general
                                 860330511787622400, # vips
                                 ]
        self.talking = {}
        self.bankers = [528555826047352833, # Kadode
                        ]
        
        # level = xp//1000
        self.level_roles ={1:875102723949854750,
                           2:958761274739679313,
                           5:879740517167009843,
                           10:874365440288239636,
                           40:878429588299067422,
                           500:892115147798220840,
                           }
        
        for level, role in self.level_roles.items():
            self.level_roles[level] = await self.bot.guild.fetch_role(role)

        await super().cog_load()

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        self.new_member(member)

    def calc_msg_xp(self, member_id: int) -> int:
        xp = random.randint(1,15)
        xp *= self.database.get_xp_multiplier(member_id)

        return int(xp//1)

    def calc_call_coins(self, member_id: int, channel) -> int:
        seconds_talking = int(datetime.datetime.now().timestamp()//1) - self.talking[member_id]

        # 5 coins per hour
        coins = 5*(seconds_talking//(60*60))

        if channel.category_id != self.call_xp_category[0]:
            coins *= 0.8

        return int(coins//1)

    def calc_call_xp(self, member_id:int, channel) -> int:
        seconds_talking = int(datetime.datetime.now().timestamp()//1) - self.talking[member_id]

        # 15xp per 10 min
        xp = 15*(seconds_talking/(10*60))
        xp *= self.database.get_xp_multiplier(member_id)

        if channel.category_id != self.call_xp_category[0]:
            xp *= 0.8

        return int(xp//1)
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        
        if message.author.id in self.in_cooldown:
            return
        
        if message.channel.id not in self.chat_xp:
            return
        
        member = message.author
        self.in_cooldown.add(member.id)

        if self.database.get(member) is None:
            self.new_member(member=member)
            
        xp = self.calc_msg_xp(member_id=member.id)
        self.database.add_xp(identifier=member.id,points=xp)
        
        await asyncio.sleep(15)
        self.in_cooldown.remove(member.id)

    async def add_call_reward(self, member: Member, channel):
        if member.id not in self.talking:
            return
        
        if self.database.get(member) is None:
            self.new_member(member)

        xp = self.calc_call_xp(member_id=member.id, channel=channel)
        coins = self.calc_call_coins(member_id=member.id, channel=channel)

        user = self.database.add_xp(identifier=member,points=xp)
        user = self.database.add_coins(identifier=member,coins=coins)

        seconds_talking = int(datetime.datetime.now().timestamp()//1) - self.talking[member.id]
        self.talking.pop(member.id, 0)

        await self.bot.log.embed(type=Log_Type.CALL,
                                 module=f"{self} (Call)",
                                 message=f"<@{member.id}>\n-# {Utils.format_seconds(seconds_talking)}\n\n+ {xp} xp\n+ {coins} moedas")

    # before.channel -> channel where member WAS
    # after.channel  -> channel where member IS
    # both (before/after).channel are updated with current status
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.bot:
            return
        
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
            await self.add_call_reward(member=member, channel=before.channel)

            members_talking_before = [m for m in before.channel.members
                                      if (not m.bot) and talking(m.voice)]
            if len(members_talking_before) == 1:
                await self.add_call_reward(member=members_talking_before[0],channel=before.channel)

        # start counting time talking when 2 or more people talking in call
        if talking(after):
            if after.channel.category_id not in self.call_xp_category:
                return

            members_talking_after = [m for m in after.channel.members 
                                    if (not m.bot) and talking(m.voice)]

            if len(members_talking_after) == 2:
                for call_member in members_talking_after:
                    self.talking[call_member.id] = now

            if len(members_talking_after) > 2:
                self.talking[member.id] = now
        
    @commands.group(name="balance",
                    aliases=["bal","atm","saldo","coins","moedas","moeda"],
                    invoke_without_command=True)
    async def balance(self, context: Context, member: Member|int = None):
        if member is None:
            member = context.author

        user = self.database.get(identifier=member)
        if user is None:
            if isinstance(member,Member):
                member = member.name
            await context.reply(f"`{member}` não casdastrado")

        await context.reply(f"{member.display_name} tem {user.coins} {"dobrão" if user.coins == 1 else "dobrões"}")

    @checks.is_banker()
    @balance.command(name="add")
    async def balance_add(self, context: Context, member: Member | int, coins: int):
        user = self.database.add_coins(identifier=member,coins=coins)
        await context.reply(f"`{user.username}` agora tem {user.coins} {"dobrão" if user.coins == 1 else "dobrões"}")

    @checks.is_banker()
    @balance.command(name="remove")
    async def balance_remove(self, context: Context, member: Member | int, coins: int):
        user = self.database.remove_coins(identifier=member,coins=coins)
        await context.reply(f"`{user.username}` agora tem {user.coins} {"dobrão" if user.coins == 1 else "dobrões"}")

    @checks.is_banker()
    @balance.command(name="edit")
    async def balance_edit(self, context: Context, member: Member | int, coins: int):
        user = self.database.set_coins(identifier=member,coins=coins)
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
    async def experience(self, context: Context, member: Member | int = None):
        if member is None:
            member = context.author
        user = self.database.get(identifier=member)
        if user is None:
            if isinstance(member,Member):
                member = member.name
            await context.reply(f"`{member}` não casdastrado")

        await context.reply(f"{member} tem {user.xp} xp")

    @checks.is_adm()
    @experience.command(name="add")
    async def experience_add(self, context: Context, member: Member| int, points: int):
        if points < 0:
            await context.send("Give a positive amount of xp")

        try:
            user = self.database.add_xp(identifier=member,points=points)
        except User_Not_Found as err:
            await context.reply(f"`{err.identifier}` não casdastrado")
            return
        
        await context.reply(f"`{user.username}` agora tem {user.xp} xp")

    @checks.is_adm()
    @experience.command(name="remove")
    async def experience_remove(self, context: Context, member: Member| int, points: int):
        if points < 0:
            await context.send("Give a positive amount of xp")
        try:
            user = self.database.remove_xp(identifier=member,points=points)
        except User_Not_Found as err:
            await context.reply(f"`{err.identifier}` não casdastrado")
            return
        
        await context.reply(f"`{user.username}` agora tem {user.xp} xp")

    @checks.is_adm()
    @experience.command(name="edit")
    async def experience_edit(self, context: Context, member: Member| int, points: int):
        try:
            user = self.database.set_xp(identifier=member,points=points)
        except User_Not_Found as err:
            await context.reply(f"`{err.identifier}` não casdastrado")
            return
        
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
            self.database.new_member(member)
        except Exception as err:
            raise(err)

    @checks.is_adm()
    @commands.command()
    async def new(self, context: Context):
        try:
            self.new_member(context.author)
        except Exception as err:
            await context.send(type(err))

    def check_level(self, member: Member):
        try:
            self.database.get_level(member.id)


            ...
        except:
            ...