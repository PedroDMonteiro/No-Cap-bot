from functools import wraps

from discord import Member, User

from database.general import Database as db
from utils.erros.database import User_Not_Found
from cogs.economy.models.user import User as md_User

from myBot import MyBot

async def setup(bot: MyBot):
    pass

def user_in_database():
    def decorator(func):
        @wraps(func)
        def wrapper(self, identifier: int | Member | User, *args, **kwargs):

            if self.get(identifier) is None:
                raise User_Not_Found(identifier)

            return func(self, identifier, *args, **kwargs)

        return wrapper
    return decorator

class Database(db):
    def new_member(self, user:Member):
        try:
            args = []
            sql=""
            sql +="\n"+f"INSERT INTO member (id, username)"
            sql +="\n"+f"values (?, ?)"
            args.append(user.id)
            args.append(user.name)

            self.update(sql,args)
        except Exception as err:
            raise (err)
    
    def get(self, identifier:int|Member|User) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id

        args = []
        sql=""
        sql +="\n"+f"SELECT username,xp,coins"
        sql +="\n"+f"FROM member"
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        row = self.select_one(sql,args)

        if row is None:
            return None

        return md_User(id=id,
                    username=row[0],
                    xp=int(row[1]),
                    coins=int(row[2]))

    def get_all(self, ) -> list[md_User]:
        sql=""
        sql +="\n"+f"SELECT id,username,xp,coins"
        sql +="\n"+f"FROM member"
        rows = self.select_all(sql)

        return [md_User(id=int(row[0]),
                    username=row[1],
                    xp=int(row[2]),
                    coins=int(row[3]),)
                for row in rows]

    @user_in_database()
    def add_coins(self, identifier: int|Member|User, coins: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id

        args = []
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET coins = coins + ?"
        args.append(coins)
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        self.update(sql,args)

        return self.get(identifier=identifier)
    
    @user_in_database()
    def remove_coins(self, identifier: int|Member|User, coins: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        args = []
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET coins = GREATEST(coins - ?, 0)"
        args.append(coins)
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        self.update(sql,args)

        return self.get(identifier=identifier)

    @user_in_database()
    def set_coins(self, identifier: int|Member|User, coins: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id

        args = []
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET coins = ?"
        args.append(coins)
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        self.update(sql,args)

        return self.get(identifier=identifier)

    def get_coins_rank(self, ) -> list[md_User]:
        sql=""
        sql +="\n"+f"SELECT id,username,xp,coins"
        sql +="\n"+f"FROM member"
        sql +="\n"+f"ORDER BY coins desc"
        rows = self.select_all(sql)

        return [md_User(id=int(row[0]),
                    username=row[1],
                    xp=int(row[2]),
                    coins=int(row[3]),)
                for row in rows]

    @user_in_database()
    def add_xp(self, identifier: int|Member|User, points: int) -> md_User:
        if self.get(identifier) is None:
            if not isinstance(identifier,Member):
                raise User_Not_Found(identifier)
            
            self.new_member(identifier)

        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        args = []
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET xp = xp + ?"
        args.append(points)
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        self.update(sql,args)

        return self.get(identifier=identifier)
    
    @user_in_database()
    def remove_xp(self, identifier: int|Member|User, points: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        args = []
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET xp = GREATEST(xp - ?, 0)"
        args.append(points)
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        self.update(sql,args)

        return self.get(identifier=identifier)
    
    @user_in_database()
    def set_xp(self, identifier: int|Member|User, points: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
        
        args = []
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET xp = ?"
        args.append(points)
        sql +="\n"+f"WHERE id = ?"
        args.append(id)

        self.update(sql,args)

        return self.get(identifier=identifier)

    def get_xp_rank(self, ) -> list[md_User]:
        sql=""
        sql +="\n"+f"SELECT id,username,xp,coins"
        sql +="\n"+f"FROM member"
        sql +="\n"+f"ORDER BY xp desc"
        rows = self.select_all(sql)

        return [md_User(id=int(row[0]),
                    username=row[1],
                    xp=int(row[2]),
                    coins=int(row[3]),)
                for row in rows]
    
    def get_xp_multiplier(self, member_id: int) -> float:
        args = []
        sql = ""
        sql += "\n"+f"SELECT v.xp_multiplier"
        sql += "\n"+f"FROM vip_member vu"
        sql += "\n"+f"LEFT JOIN vips v on v.id = vu.vip_id "
        sql += "\n"+f"WHERE vu.member_id = ?"
        args.append(member_id)
        sql += "\n"+f"AND active = TRUE"

        row = self.select_one(sql,args)

        if row is None:
            return 1.0

        return float(row[0])

    @user_in_database()
    def get_level(self, identifier: int|Member|User) -> int:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
        args = []
        sql = ""
        sql += "\n"+f"SELECT xp"
        sql += "\n"+f"FROM member"
        sql += "\n"+f"WHERE id = ?"
        args.append(identifier)

        row = self.select_one(sql,args)

        xp = int(row[0])

        return int(xp//1000)