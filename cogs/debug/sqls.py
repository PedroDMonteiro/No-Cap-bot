from discord import Member, User

from database.general import Database as db
from utils.erros.database import User_Not_Found
from models.user import User as md_User

from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def delete_member(self, to_delete:list[int]):
        if len(to_delete) == 0:
            return

        try:
            sql=""
            sql +="\n"+f"DELETE FROM member"
            sql +="\n"+f"WHERE id in ({",".join(map(str,to_delete))})"
            print(sql)
            self.update(sql)
        except Exception as err:
            raise (err)