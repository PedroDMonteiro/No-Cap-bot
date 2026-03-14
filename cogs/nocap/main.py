from io import BytesIO
import random
import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Bot,Cog
from utils.configuration import CHAT_GERAL_ID
from discord import File, Member,Message

from myBot import MyBot

async def setup(bot: Bot):
    await bot.add_cog(Cog_NoCap(bot))

class Cog_NoCap(Cog, name= "NoCap"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        # self.database = db()
        self.msg_count = 0

    async def cog_load(self):
        print(f"{self.__cog_name__} is up")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot:
            if message.guild:
                if message.channel.id == CHAT_GERAL_ID:
                    self.msg_count += 1
                    if random.randint(1,200) == 1 and self.msg_count > 100:
                        self.msg_count = 0
                        text = random.choices(population=['la ele','la ela','foi o q ela disse','foi o q ele disse'],
                                weights=[0.16,0.36,0.25,0.23])[0]
                        await message.reply(text)
        
    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        # Check if the "Server Booster" role was added to the member
        if discord.utils.get(after.roles, name="Booster"):
            if not discord.utils.get(before.roles, name="Booster"):
                print(f"{after.display_name} has boosted the server!")
            # You can add your custom actions here, e.g., send a message to a channel
            # channel = bot.get_channel(YOUR_CHANNEL_ID)
            # await channel.send(f"Thanks for boosting, {after.mention}!")

    @commands.command()
    async def banner(self, context: Context, user: Member = None):
        if user is None:
            user = context.author

        print(user.guild_avatar)
        print(user.guild_banner)
        if user.banner is None:
            await context.send(f"{user.display_name} não tem banner.")
            return
        
        extension = 'png'
        if user.banner.is_animated():
            extension = 'gif'
        banner = File(fp=BytesIO(await user.banner.read()),filename=f"banner.{extension}")

        await context.send(files=[banner])
        



#expressões
# Quem muito fala, da o cu para o pipoqueiro.
# Desconfia mais, jaja ta dando o cu para o porteiro.
# Se você não comer o bolo agora, ninguém vai guardar para vc comer depois\n-# não é sobre bolos
# Peida na minha cara, mas não suja meu bigode
# Quem olha para baixo tem depressão
# Xerecas confusas machucam xibatas incríveis
# Deus fez as primas para nós não comermos as avós
# Quem tem pena é galinha, tu é piranha!
# Quer moleza, senta no pudim
# Vc é um fracasso, um fracasso na tentativa de ser um merda, VC É MEU IDALO



#cantadas
# Você sempre foi gostosa assim ou você ta fantasiada de lasanha?

#curiosidades
# O que o batman faz quando ta com tesão? # ELE DA O CU.
# Engravidar em video chamadas, segundo especialistas, continua sendo mito
# Filmes independentes são em preto e branco de cowboys gays comendo pudim
# # Noticia: Kiko faz show no Piru!!