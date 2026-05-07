from database.general import Database as db
from utils.erros.database import *

from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def get_random_frase(self) -> str:

        sql = ""
        sql += "\n"+f"SELECT content"
        sql += "\n"+f"FROM frase"
        sql += "\n"+f"ORDER BY RAND() LIMIT 1;"
        row = self.select_one(sql)
        return row[0]