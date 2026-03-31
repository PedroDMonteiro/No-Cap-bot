from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import Bot,Cog

from log import Log_Type
from myBot import MyBot
from cogs.database.sqls import Database as db
from utils import checks
from utils.erros.database import Table_Not_Found

async def setup(bot: Bot):
    await bot.add_cog(Cog_Database(bot))

class Cog_Database(Cog, name= "Database"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.msg_count = 0
        self.database = db()

    async def cog_load(self):
        print(f"{self.__cog_name__} is up")

    @commands.command(name="sql")
    @checks.is_developer()
    async def sql(self, context: Context, *args) -> None:
        query = " ".join(args)

        if query == "":
            await context.send("query needed")

        rows = []
        try:
            initial = query[:10].lower()
            if initial.startswith("select"):
                rows = self.database.select_all(query)
            else:
                self.database.update(query)
        except Exception as err:
            await self.bot.log.embed(type=Log_Type.ERROR,
                                     module=self.__cog_name__,
                                     message=f"Erro na query `{query}`:\n{err}")
            return

        await context.send(f"` {query} `")
        if len(rows) == 0:
            initial = query[:10].lower()
            if initial.startswith("select"):
                await context.send(f"` No match found `")
            else:
                await context.send("` Database Updated `")
                return

        for row in rows:
            await context.send(f"`{row}`")

    @commands.command()
    async def table(self, context: Context, table: str) -> None:
        try:
            columns, rows = self.database.table(table)
        except Exception as err:
            if isinstance(err,Table_Not_Found):
                await context.send(f"` {table.upper()} not found `")
                return
            
            raise err

        await context.send(f"` {table.upper()} `")
        await context.send(f"` Linhas: {len(rows)} `")
        await context.send(f"` {','.join(columns)} `")
        for row in rows:
            await context.send(f"` {row} `")

    @commands.command(name="database",
                      aliases=["db"])
    async def database_command(self, context: Context) -> None:
        ...
