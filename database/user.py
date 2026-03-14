from typing import Union
from discord import Member, User as dc_User
from models.user import User
from database import general as db
from utils.erros.database import *

def add(member:Member) -> User:
    try:
        sql=""
        sql +="\n"+f"INSERT INTO user"
        sql +="\n"+f"(id,username) VALUES"
        sql +="\n"+f"('{member.id}','{member.name}')"
        db.update(sql)

        return get(identifier=member)
    except Exception as err:
        raise (err)
    
def get(identifier:int|Member|dc_User) -> User:
    if isinstance(identifier,int):
        id = identifier
    else:
        id = identifier.id

    sql=""
    sql +="\n"+f"SELECT username,xp,coins"
    sql +="\n"+f"FROM user"
    sql +="\n"+f"WHERE id = '{id}'"
    row = db.select_one(sql)

    if row is None:
        raise User_Not_Found(identifier=identifier)

    return User(id=id,
                username=row[0],
                xp=int(row[1]),
                coins=int(row[2]))

def get_all() -> list[User]:
    sql=""
    sql +="\n"+f"SELECT id,username,xp,coins"
    sql +="\n"+f"FROM user"
    rows = db.select_all(sql)

    return [User(id=int(row[0]),
                username=row[1],
                xp=int(row[2]),
                coins=int(row[3]),)
            for row in rows]

def add_coins(identifier: int|Member|dc_User, coins: int) -> User:
    if isinstance(identifier,int):
        id = identifier
    else:
        id = identifier.id
        
    sql=""
    sql +="\n"+f"UPDATE user"
    sql +="\n"+f"SET coins = GREATEST(coins + {coins}, 0)"
    sql +="\n"+f"WHERE id = '{id}'"
    db.update(sql)

    return get(identifier=identifier)

def edit_coins(identifier: int|Member|dc_User, coins: int) -> User:
    if isinstance(identifier,int):
        id = identifier
    else:
        id = identifier.id

    sql=""
    sql +="\n"+f"UPDATE user"
    sql +="\n"+f"SET coins = {coins}"
    sql +="\n"+f"WHERE id = '{id}'"
    db.update(sql)

    return get(identifier=identifier)

def get_coins_rank() -> list[User]:
    sql=""
    sql +="\n"+f"SELECT id,username,xp,coins"
    sql +="\n"+f"FROM user"
    sql +="\n"+f"ORDER BY coins desc"
    rows = db.select_all(sql)

    return [User(id=int(row[0]),
                username=row[1],
                xp=int(row[2]),
                coins=int(row[3]),)
            for row in rows]

def add_xp(identifier: int|Member|dc_User, points: int) -> User:
    if isinstance(identifier,int):
        id = identifier
    else:
        id = identifier.id
        
    sql=""
    sql +="\n"+f"UPDATE user"
    sql +="\n"+f"SET xp = GREATEST(xp + {points}, 0)"
    sql +="\n"+f"WHERE id = '{id}'"
    db.update(sql)

    return get(identifier=identifier)

def edit_xp(identifier: int|Member|dc_User, points: int) -> User:
    if isinstance(identifier,int):
        id = identifier
    else:
        id = identifier.id
        
    sql=""
    sql +="\n"+f"UPDATE user"
    sql +="\n"+f"SET xp = {points}"
    sql +="\n"+f"WHERE id = '{id}'"
    db.update(sql)

    return get(identifier=identifier)


def get_xp_rank() -> list[User]:
    sql=""
    sql +="\n"+f"SELECT id,username,xp,coins"
    sql +="\n"+f"FROM user"
    sql +="\n"+f"ORDER BY xp desc"
    rows = db.select_all(sql)

    return [User(id=int(row[0]),
                username=row[1],
                xp=int(row[2]),
                coins=int(row[3]),)
            for row in rows]

def bump(identifier: Member) -> User:
    add_coins(identifier=identifier,coins=10)

    return get(identifier=identifier)