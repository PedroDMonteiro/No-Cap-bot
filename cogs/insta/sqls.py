from database.general import Database as db
from models.insta import Insta, Comment
from models.insta_rank import Insta_Rank
from utils.erros.database import *

from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def add_insta(self, message_id:int, user_id:int):
        try:
            args = []
            sql=""
            sql +="\n"+f"INSERT INTO INSTA"
            sql +="\n"+f"(message_id,user_id) VALUES"
            sql +="\n"+f"(?,?)"
            args.append(message_id)
            args.append(user_id)

            self.update(sql,args)
        except Exception as err:
            raise (err)

    # add like and return num of current likes
    def add_like(self, message_id:int, user_id:int) -> int:
        try:
            args = []
            sql=""
            sql +="\n"+f"INSERT INTO INSTA_LIKE"
            sql +="\n"+f"(message_id,user_id) values"
            sql +="\n"+f"(?,?)"
            args.append(message_id)
            args.append(user_id)
            
            self.update(sql,args)
        except Primary_Key_Duplicate as err:
            raise err
        except Exception as err:
            print(type(err))
            raise err
        
        args = []
        sql=""
        sql +="\n"+f"SELECT count(*)"
        sql +="\n"+f"FROM insta_like"
        sql +="\n"+f"WHERE message_id = ?"
        sql +="\n"+f"GROUP BY message_id"
        args.append(message_id)

        row = self.select_one(sql,args)

        return int(row[0])

    def add_comment(self, message_id:int, user_id: int, comment: str):
        max_len_comment = 30
        if len(comment) > max_len_comment:
            raise Exception(f"Máximo de {max_len_comment} caracteres")
        
        try:
            args = []
            sql=""
            sql +="\n"+f"INSERT INTO insta_comment"
            sql +="\n"+f"(message_id,user_id,comment) values"
            sql +="\n"+f"(?,?,?)"
            args.append(message_id)
            args.append(user_id)
            args.append(comment)

            self.update(sql,args)
        except Primary_Key_Duplicate as err:
            raise Exception("Você já comentou")
        except Exception as err:
            raise(err)
        
        args = []
        sql=""
        sql +="\n"+f"SELECT count(*)"
        sql +="\n"+f"FROM insta_comment"
        sql +="\n"+f"WHERE message_id = ?"
        args.append(message_id)
        sql +="\n"+f"GROUP BY message_id"

        row = self.select_one(sql,args)

        return int(row[0])
        
    def get_all_messages_id(self, ) -> list[int]:
        sql = ""
        sql += "\n"+f"SELECT message_id"
        sql += "\n"+f"FROM insta"

        return [int(row[0]) for row in self.select_all(sql)]

    def get_by_message_id(self, message_id: int) -> Insta:
        args = []
        sql = ""
        sql += "\n"+f"SELECT user_id"
        sql += "\n"+f"FROM insta "
        sql += "\n"+f"WHERE message_id = ?"
        args.append(message_id)

        user_id = int(self.select_one(sql,args)[0])

        args = []
        sql = ""
        sql += "\n"+f"SELECT il.user_id"
        sql += "\n"+f"FROM insta_like il"
        sql += "\n"+f"JOIN insta i on i.message_id = il.message_id"
        sql += "\n"+f"WHERE il.message_id = ?"
        args.append(message_id)

        likes: list[int] = []
        for row in self.select_all(sql,args):
            likes.append(int(row[0]))

        args = []
        sql = ""
        sql += "\n"+f"SELECT user_id"
        sql += "\n"+f",comment"
        sql += "\n"+f"FROM insta_comment"
        sql += "\n"+f"WHERE message_id = ?"
        args.append(message_id)

        comments: list[Comment] = []
        for row in self.select_all(sql,args):
            comments.append(Comment(user_id=int(row[0]),
                                    content=row[1]))

        return Insta(user_id=user_id,
                    message_id=message_id,
                    likes=likes,
                    comments=comments)


    def delete(self, message_id: int):
        args = []
        sql = ""
        sql += "\n"+f"DELETE FROM insta_like"
        sql += "\n"+f"WHERE message_id = ?"
        args.append(message_id)

        self.update(sql,args)

        args = []
        sql = ""
        sql += "\n"+f"DELETE FROM insta_comment"
        sql += "\n"+f"WHERE message_id = ?"
        args.append(message_id)

        self.update(sql,args)

        args = []
        sql = ""
        sql += "\n"+f"DELETE FROM insta"
        sql += "\n"+f"WHERE message_id = ?"
        args.append(message_id)

        self.update(sql,args)

    def clear(self, ):
        sql = ""
        sql += "DELETE FROM insta_like"
        self.update(sql)

        sql = ""
        sql += "DELETE FROM insta_comment"
        self.update(sql)

        sql = ""
        sql += "DELETE FROM insta"
        self.update(sql)

    def get_candidates_to_win(self, )-> list[int]:
        sql = ""
        sql += "\n"+f"SELECT likes, comments"
        sql += "\n"+f"FROM view_insta_rank "
        sql += "\n"+f"WHERE rank = 1"
        
        row = self.select_one(sql)
        
        if row is None:
            return []
        
        winner_likes = int(row[0])
        winner_comments = int(row[1])

        args = []
        sql = ""
        sql += "\n"+f"SELECT message_id"
        sql += "\n"+f"FROM view_insta_rank"
        sql += "\n"+f"WHERE likes = ?"
        args.append(winner_likes)
        sql += "\n"+f"AND comments = ?"
        args.append(winner_comments)

        rows = self.select_all(sql,args)

        return [int(row[0]) for row in rows]

    def get_ordered_rank(self, ) -> list[Insta_Rank]:
        sql = ""
        sql += "\n"+f"SELECT user_id,message_id,rank,likes,comments"
        sql += "\n"+f"FROM view_insta_rank "
        rows = self.select_all(sql)

        return [Insta_Rank(user_id=int(row[0]),
                        message_id=int(row[1]),
                        rank=int(row[2]),
                        num_likes=int(row[3]),
                        num_comments=int(row[4]),
                        ) for row in rows]