from database.general import Database as db
from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def bumped(self, member_id:int):
        try:
            args = []
            sql=""
            sql +="\n"+f"UPDATE member"
            sql +="\n"+f"SET coins = coins + 10"
            sql +="\n"+f"WHERE id = ?"
            args.append(member_id)
            
            self.update(sql,args)
        except Exception as err:
            raise (err)
