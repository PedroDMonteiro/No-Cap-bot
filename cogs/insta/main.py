import asyncio
import datetime
from io import BytesIO
import os
import requests

from discord.ext import commands,tasks
from discord.ext.commands.context import Context

from discord import File, Member, Message


from cogs.insta.models.insta import Insta
from log import Log_Type
from myBot import MyBot
from utils import checks
from utils.configuration import EMOJIS
from utils.cog import Cog

from cogs.insta.sqls import Database as db
from cogs.insta.embeds import Embeds
from cogs.insta.views import Post

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Insta(bot))

MOD_ROLE = 960707548514775070
MOD_ROLE = 'Insta-Mod'

class Cog_Insta(Cog, name = "Insta"):
    CHANNEL_ID = 1135931353720963072
    ROLE = 893650528981098558
    
    async def cog_load(self):
        self.database = db()
        # Registrar a view persistente
        self.bot.add_view(Post())
        self.channel = await self.bot.fetch_channel(Cog_Insta.CHANNEL_ID)
        self.emoji_insta = await self.bot.fetch_application_emoji(EMOJIS['insta'])
        self.insta_loop.start()
        
        await super().cog_load()
    
    async def get_current_winner(self) -> tuple[Member,Insta]:
        guild = self.bot.get_guild(self.bot.guild_id)

        posts = self.database.get_all()
        posts = sorted(posts,reverse=True)
        for post in posts:
            winner = await guild.fetch_member(post.user_id)
            if winner:
                return winner, post
            
        return None

    async def save_winner(self, winner: Insta, delete_olds: bool = False) -> str:
        dir = "cogs/insta/winner"
        if delete_olds:
            to_remove = sorted([filename for filename in os.listdir(dir) if os.path.isfile(f"{dir}/{filename}")])[4:]
            for file in to_remove:
                os.remove(file)

        path = f"{dir}/{int(datetime.datetime.now().timestamp()//1)}.{winner.extension}"

        message = await self.channel.fetch_message(winner.message_id)

        def save_file():
            buffer = BytesIO(requests.get(message.attachments[0].url).content)
            with open(path, "wb") as binary_file:
                binary_file.write(buffer.getvalue())
        await asyncio.to_thread(save_file)

        return path
    
    async def clear_posts(self):
        for message_id in self.database.get_all_messages_id():
            try:
                await (await self.channel.fetch_message(message_id)).delete()
            except Exception as err:
                await self.bot.log.embed(type=Log_Type.ERROR,
                                         module=self,
                                         message=f"Error to delete insta message: {err}")

        self.database.clear()

    async def update_role(self, winner: Member):
        role = self.bot.get_guild(self.bot.guild_id).get_role(Cog_Insta.ROLE)
        for member in role.members:
            await member.remove_roles(role)
        await winner.add_roles(role)

    async def define_winner(self):
        try:
            winner_member, winner_post = await  self.get_current_winner()
            if winner_member is None:
                await self.bot.log.embed(type=Log_Type.DEFAULT,module=self,message="Nenhum post tem usuário válido no servidor")
                return

            await self.update_role(winner_member)

            path = await self.save_winner(winner_post)

            embed, files = Embeds.winner(winner=winner_member,
                                         likes=winner_post.num_likes(),
                                         path=path,
                                         extension=winner_post.extension)

            await self.channel.send(f"<@{winner_member.id}>",embed=embed,files=files)

            await self.clear_posts()
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,
                                     module=self,
                                     message=f"Error to define winner: {err}")
            
    async def simulate_winner(self, context: Context):
        try:
            winner_member, winner_post = await  self.get_current_winner()
            if winner_member is None:
                await self.bot.log.embed(type=Log_Type.DEFAULT,module=self,message="Nenhum post tem usuário válido no servidor")
                return

            path = await self.save_winner(winner_post,delete_olds=False)

            embed, files = Embeds.winner(winner=winner_member,
                                         likes=winner_post.num_likes(),
                                         path=path,
                                         extension=winner_post.extension)

            await context.send(f"<@{winner_member.id}>",embed=embed,files=files)

            os.remove(path)
            
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,
                                     module=self,
                                     message=f"Error in simulate winner: {err}")

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

    async def create_post(self, message: Message):
        text = ""
        text += f"<@{message.author.id}>"
        if len(message.content) > 0:
            text += f"\n> {message.content.replace("\n","\n> ")}"

        try:
            file = await message.attachments[0].to_file()
            extension = file.filename.split(".")[1]
        except Exception as err:
            self.bot.log.embed(Log_Type.ERROR,module=self,message=f"Erro ao criar post: {err}")
            await message.reply("Houve algo de errado com sua foto, mande novamente",delete_after=5)
            return

        insta_message = await message.channel.send(text,file=file,view=Post())
        self.database.add_post(message_id=insta_message.id,
                               user_id=message.author.id,
                               extension=extension)
    
    async def send_help(self, member: Member):
        try:
            await member.send(f"Mande sua foto com alguma descrição em <#{self.channel.id}>\nEu tomo conta do resto :wink:")
        except Exception as err:
            print(member)
            await self.bot.log.embed(Log_Type.ERROR,module=self,message=f"Erro ao mandar help: {err}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == self.bot.user.id:
            return
        
        if message.channel.id == Cog_Insta.CHANNEL_ID:
            if len(message.attachments) == 0:
                await self.send_help(message.author)
            else:
                await self.create_post(message)

            try:
                await message.delete()
            except:
                pass
                #message already deleted

    @commands.group(invoke_without_command=True)
    async def insta(self, context: Context):
        ...

    @insta.command()
    @checks.is_adm()
    async def update(self, context: Context):
        ...

    @insta.group(invoke_without_command=True)
    @checks.is_adm()
    async def winner(self, context: Context):
        await self.define_winner()
        await context.reply("Vencedor atualizado",mention_author=False)

    @winner.command(name="check")
    @checks.is_adm()
    async def winner_check(self, context: Context):
        await self.simulate_winner(context)

    @winner.command(name="simulate")
    @checks.is_adm()
    async def winner_simulate(self, context: Context):
        ...

    @insta.command()
    @checks.is_adm()
    async def check(self, context: Context):
        try:
            guild = self.bot.get_guild(self.bot.guild_id)
            winner = await self.get_winner()
            if winner is None:
                return
            
            winner_member = await guild.fetch_member(winner.user_id)
            winner_message = await self.channel.fetch_message(winner.message_id)
            extension = winner_message.attachments[0].url.split("?")[0].split("/")[-1].split(".")[-1]
            print(extension)
            def save_file():
                buffer = BytesIO(requests.get(winner_message.attachments[0].url).content)
                with open(f"cogs/insta/winner.{extension}", "wb") as binary_file:
                    binary_file.write(buffer.getvalue())
            await asyncio.to_thread(save_file)

            winner_file = File(f"cogs/insta/winner.{extension}",filename=f"insta.{extension}")
            await self.bot.log.embed(type=Log_Type.DEBUG,
                                     module=self,
                                     message=f"Next winner {winner_member}",
                                     file=winner_file)
            
            os.remove(f"cogs/insta/winner.{extension}")
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,
                                     module=self,
                                     message=f"Error to define winner: {err}")