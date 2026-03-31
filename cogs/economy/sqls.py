from discord import Member, User

from database.general import Database as db
from utils.erros.database import User_Not_Found
from models.user import User as md_User

from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def new_member(self, user:Member):
        try:
            sql=""
            sql +="\n"+f"INSERT INTO member (id,username,coins)"
            sql +="\n"+f"values ('{user.id}', '{user.name}',100)"
            self.update(sql)
        except Exception as err:
            raise (err)
        
    def get(self, identifier:int|Member|User) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id

        sql=""
        sql +="\n"+f"SELECT username,xp,coins"
        sql +="\n"+f"FROM member"
        sql +="\n"+f"WHERE id = '{id}'"
        row = self.select_one(sql)

        if row is None:
            raise User_Not_Found(identifier=identifier)

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

    def add_coins(self, identifier: int|Member|User, coins: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET coins = coins + {coins}"
        sql +="\n"+f"WHERE id = '{id}'"
        self.update(sql)

        return self.get(identifier=identifier)
    
    def remove_coins(self, identifier: int|Member|User, coins: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET coins = GREATEST(coins - {coins}, 0)"
        sql +="\n"+f"WHERE id = '{id}'"
        self.update(sql)

        return self.get(identifier=identifier)

    def set_coins(self, identifier: int|Member|User, coins: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id

        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET coins = {coins}"
        sql +="\n"+f"WHERE id = '{id}'"
        self.update(sql)

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

    def add_xp(self, identifier: int|Member|User, points: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET xp = xp + {points}"
        sql +="\n"+f"WHERE id = '{id}'"
        self.update(sql)

        return self.get(identifier=identifier)
    
    def remove_xp(self, identifier: int|Member|User, points: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET xp = GREATEST(xp - {points}, 0)"
        sql +="\n"+f"WHERE id = '{id}'"
        self.update(sql)

        return self.get(identifier=identifier)
    
    def set_xp(self, identifier: int|Member|User, points: int) -> md_User:
        if isinstance(identifier,int):
            id = identifier
        else:
            id = identifier.id
            
        sql=""
        sql +="\n"+f"UPDATE member"
        sql +="\n"+f"SET xp = {points}"
        sql +="\n"+f"WHERE id = '{id}'"
        self.update(sql)

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

