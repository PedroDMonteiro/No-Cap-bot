import datetime

from discord import Embed, File, Member, Message, VoiceState
from discord.ext import commands
from discord.ext.commands.context import Context

from log import Log_Type
from myBot import MyBot
from utils.cog import Cog
from utils import checks
from utils import utils

from cogs.economy.sqls import Database as economy_db
from cogs.debug.sqls import Database as db

async def setup(bot: MyBot):
    await bot.add_cog(Cog_Debug(bot))

class Cog_Debug(Cog, name= "Debug"):
    async def cog_load(self):
        self.economy_database = economy_db()
        self.database = db()
        await super().cog_load()

    @commands.command(name="debug")
    @checks.is_developer()
    async def debug(self, context: Context, cog_name: str, attribute_name: str) -> None:
        cog_instance = self.bot.get_cog(cog_name) # The name here is the class name

        if cog_instance:
            # Access the shared parameter
            param_value = getattr(cog_instance, attribute_name)
            await context.send(f"{cog_name}.{attribute_name}:")
            if utils.Utils.is_iterable(param_value):
                await context.send("[")
                for v in param_value:
                    await context.send(v)
                await context.send("]")
        else:
            await context.send(f"{cog_name} not found or not loaded.")
    
    @commands.command()
    async def nick(self, context: Context, member: Member = None):
        user = context.author
        if member:
            user = member
        await context.reply(f"{user.global_name=}")
        await context.reply(f"{user.display_name=}")
        await context.reply(f"{user.name=}")
        await context.reply(f"{user.nick=}")

    @commands.command()
    @checks.is_developer()
    async def test(self, context: Context):
        t = int(datetime.datetime.now().timestamp()//1)
        await context.send(len(str(t)))
        embed = Embed(title="Teste")
        winner_file = File(f"./cogs/debug/bernardo.webp",filename=f"insta.webp")

        embed.set_image(url=f"attachment://{winner_file.filename}")
        msg = await context.send(embed=embed,file=winner_file)
        await context.send(msg.embeds[0].image.url)

    @commands.command()
    @checks.is_developer()
    async def check_members(self, context: Context):
        users_db = [user.id for user in self.economy_database.get_all()]
        bots_db = []
        for member in context.guild.members:
            if member.bot and member.id in users_db:
                bots_db.append(member.id)

        await context.send(f"Bots no banco: {bots_db}")

        try:
            self.database.delete_member(bots_db)
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,
                               module=self.__cog_name__,
                               message=f"Error no check de usuarios: {err}")
            return
        await context.send(f"Bots removidos")

    @commands.command()
    @checks.is_developer()
    async def check_sql(self, context: Context):
        sql = "select *"
        sql += "\n"+f"FROM member"
        sql += "\n"+f"WHERE username like ?"
        rows = self.database.select_one(sql,[f"%pessimista%"])
        
        await context.send(f"{rows}")