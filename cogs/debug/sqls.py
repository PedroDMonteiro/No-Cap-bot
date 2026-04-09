from database.general import Database as db

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
            self.update(sql)
        except Exception as err:
            raise (err)