import random
from io import BytesIO

from discord import File, Member,Message
from discord.ext import commands
from discord.ext.commands.context import Context

from myBot import MyBot
from utils.cog import Cog

from cogs.miscellaneous.sqls import Database as db

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Miscellaneous(bot))

class Cog_Miscellaneous(Cog, name= "Miscellaneous"):
    async def cog_load(self):
        self.CHAT_GERAL_ID = 866894423164846110
        self.msg_count = 0
        self.database = db()
        await super().cog_load()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.author.bot:
            if message.guild:
                if message.channel.id == self.CHAT_GERAL_ID:
                    self.msg_count += 1
                    if random.randint(1,200) == 1 and self.msg_count > 100:
                        self.msg_count = 0
                        text = random.choices(population=['la ele','la ela','foi o q ela disse','foi o q ele disse'],
                                weights=[0.16,0.36,0.25,0.23])[0]
                        await message.reply(text)

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
        
    @commands.command(name="silvio",aliases=["frases"])
    async def silvio(self, context: Context):
        frase = self.database.get_random_frase()
        await context.reply(frase)

#cantadas
# 