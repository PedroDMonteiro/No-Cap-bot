from database.general import Database as db
from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def bumped(self, user_id:int):
        try:
            sql=""
            sql +="\n"+f"UPDATE USER"
            sql +="\n"+f"SET coins = coins + 10"
            sql +="\n"+f"WHERE id = '{user_id}'"
            self.update(sql)
        except Exception as err:
            raise (err)
