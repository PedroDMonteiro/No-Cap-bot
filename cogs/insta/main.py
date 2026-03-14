import asyncio
import datetime
from io import BytesIO
import os
import requests

from discord.ext import commands,tasks
from discord.ext.commands import Cog
from discord.ext.commands.context import Context

from discord import Embed, File, Message


from myBot import MyBot
from models.insta_rank import Insta_Rank
from utils.configuration import EMOJIS
from cogs.insta.sqls import Database as db
from cogs.insta.views import Post

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Insta(bot))

MOD_ROLE = 960707548514775070
MOD_ROLE = 'Insta-Mod'

class Cog_Insta(Cog, name = "Insta"):
    CHANNEL_ID = 1135931353720963072
    LOG_CHANNEL_ID = 1412278637528350840
    ROLE = 893650528981098558

    def __init__(self, bot: MyBot):
        self.bot = bot
        self.database = db()

    async def cog_load(self):
        # Registrar a view persistente
        self.bot.add_view(Post())
        self.channel = await self.bot.fetch_channel(Cog_Insta.CHANNEL_ID)
        self.log_channel = await self.bot.fetch_channel(Cog_Insta.LOG_CHANNEL_ID)
        self.emoji_insta = await self.bot.fetch_application_emoji(EMOJIS['insta'])
        self.insta_loop.start()
        print(f"{self.__cog_name__} is up")
    
    async def get_winner(self) -> Insta_Rank:
        guild = self.bot.get_guild(MyBot.MAIN_GUILD)

        winners = self.database.get_ordered_rank()
        for winner_rank in winners:
            winner = await guild.fetch_member(winner_rank.user_id)
            if winner:
                return winner_rank

    async def define_winner(self):
        try:
            winner = await self.get_winner()
            if winner is None:
                return
            
            winner_member = await self.bot.get_guild(MyBot.MAIN_GUILD).fetch_member(winner.user_id)

            role = self.bot.get_guild(MyBot.MAIN_GUILD).get_role(Cog_Insta.ROLE)
            for member in role.members:
                await member.remove_roles(role)

            await winner_member.add_roles(role)
            
            winner_message = await self.channel.fetch_message(winner.message_id)
            extension = winner_message.attachments[0].url.split("?")[0].split("/")[-1].split(".")[-1]
            
            def save_file():
                buffer = BytesIO(requests.get(winner_message.attachments[0].url).content)
                with open(f"cogs/insta/winner.{extension}", "wb") as binary_file:
                    binary_file.write(buffer.getvalue())
            await asyncio.to_thread(save_file)
            winner_file = File(f"cogs/insta/winner.{extension}",filename=f"insta.{extension}")

            message = await self.log_channel.send(f"Winner {winner}", files=[winner_file])
            winner_file_url = message.attachments[0].url

            embed = Embed(title="",description=f"{winner_member.mention} está mais perto de ter sua estrela na calçada da fama\n\n<:heart:{EMOJIS['heart']}> **{winner.num_likes}**")
            embed.set_author(name=f'{winner_member.display_name}',icon_url=self.emoji_insta.url)
            embed.set_thumbnail(url=winner_member.avatar.url)
            embed.color = 0xBB1313
            embed.set_image(url=winner_file_url)
            await self.channel.send(f"<@{winner.user_id}>",embed=embed)
            # embed.set_image(url=f"attachment://{winner_file.filename}")
            # await channel.send(f"<@{winner.id}>",embed=embed,files=[winner_file])

            for message_id in self.database.get_all_messages_id():
                try:
                    await (await self.channel.fetch_message(message_id)).delete()
                except:
                    print("Erro delete insta msg")

            self.database.clear()

            os.remove(f"cogs/insta/winner.{extension}")
        except Exception as err:
            print(err)

    @tasks.loop(time=datetime.time(hour=19))
    async def insta_loop(self) -> None:
        # 0 -> monday
        # 6 -> sunday
        match datetime.datetime.now().weekday():
            case 2: # quarta
                await self.channel.send('@everyone',delete_after=0.5)
            case 4: # sexta
                await self.channel.send('@here',delete_after=0.5)
            case 6: # domingo
                await self.define_winner()
            case _:
                return

    @insta_loop.before_loop
    async def before_update_bot(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == self.bot.user.id:
            return
        
        if message.channel.id == Cog_Insta.CHANNEL_ID:
            if len(message.attachments) > 0:
                text = ""
                text += f"<@{message.author.id}>"
                if len(message.content) > 0:
                    text += f"\n> {message.content.replace("\n","\n> ")}"
                try:
                    file = await message.attachments[0].to_file()
                except Exception as err:
                    print(f"Erro ao pegar arquivo\n{err}")
                insta_message = await message.channel.send(text,file=file,view=Post())
                self.database.add_insta(message_id=insta_message.id,
                                        user_id=message.author.id)
            await message.delete()

    @commands.command()
    @commands.check_any(commands.has_role(MOD_ROLE),
                        commands.has_permissions(administrator=True))
    async def insta_winner(self, context: Context):
        await self.define_winner()
        await context.reply("Vencedor atualizado",mention_author=False)