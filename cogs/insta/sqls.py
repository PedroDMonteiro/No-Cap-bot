from database.general import Database as db
from cogs.insta.models.insta import Insta, Comment
from utils.erros.database import *

from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def add_post(self, message_id:int, user_id:int, extension: str):
        try:
            args = []
            sql=""
            sql +="\n"+f"INSERT INTO INSTA"
            sql +="\n"+f"(message_id,user_id,extension) VALUES"
            sql +="\n"+f"(?,?,?)"
            args.append(message_id)
            args.append(user_id)
            args.append(extension)

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
        
        return len(self.get_likes(message_id=message_id))

    def add_comment(self, message_id:int, user_id: int, comment: str) -> int:
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

        return len(self.get_comments(message_id=message_id))
        
    def get_all(self, limit: int = None) -> list[Insta]:
        args = []
        sql = ""
        sql += "\n"+f"SELECT message_id,user_id,extension"
        sql += "\n"+f"FROM insta"
        if limit:
            sql += "\n"+f"LIMIT ?"
            args.append(limit)

        posts: list[Insta] = []
        
        for row in self.select_all(sql):
            message_id = int(row[0])
            posts.append(Insta(message_id=message_id,
                               user_id=int(row[1]),
                               extension=row[2],
                               likes=self.get_likes(message_id),
                               comments=self.get_comments(message_id)))
            
        return posts

    def get_by_message_id(self, message_id: int) -> Insta:
        args = []
        sql = ""
        sql += "\n"+f"SELECT user_id,extension"
        sql += "\n"+f"FROM insta"
        sql += "\n"+f"WHERE message_id = ?"
        args.append(message_id)

        row = self.select_one(sql,args)
        if row is None:
            return None

        return Insta(user_id=int(row[0]),
                     message_id=message_id,
                     extension=row[1],
                     likes=self.get_likes(message_id),
                     comments=self.get_comments(message_id))

    def get_likes(self, message_id: int) -> list[Comment]:
        args = []
        sql = ""
        sql += "\n"+f"SELECT il.user_id"
        sql += "\n"+f"FROM insta_like il"
        sql += "\n"+f"WHERE il.message_id = ?"
        args.append(message_id)

        likes: list[int] = []
        for row in self.select_all(sql,args):
            likes.append(int(row[0]))

        return likes

    def get_comments(self, message_id: int) -> list[Comment]:
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
            
        return comments

    def delete(self, message_id: int = None) -> None:
        args = []
        sql = ""
        sql += "\n"+f"DELETE FROM insta_like"
        if message_id:
            sql += "\n"+f"WHERE message_id = ?"
            args.append(message_id)

        self.update(sql,args)

        args = []
        sql = ""
        sql += "\n"+f"DELETE FROM insta_comment"
        if message_id:
            sql += "\n"+f"WHERE message_id = ?"
            args.append(message_id)

        self.update(sql,args)

        args = []
        sql = ""
        sql += "\n"+f"DELETE FROM insta"
        if message_id:
            sql += "\n"+f"WHERE message_id = ?"
            args.append(message_id)

        self.update(sql,args)

    def clear(self, ) -> None:
        self.delete()

    def get_ordered_rank(self, limit: int = None) -> list[Insta]:
        args = []
        sql = ""
        sql += "\n"+f"SELECT user_id,message_id,rank"
        sql += "\n"+f"FROM view_insta_rank "
        if limit:
            sql += "\n"+f"LIMIT ?"
            args.append(limit)

        rows = self.select_all(sql,args)

        return [Insta(user_id=int(row[0]),
                        message_id=int(row[1]),
                        rank=int(row[2]),
                        extension="",
                        ) for row in rows]