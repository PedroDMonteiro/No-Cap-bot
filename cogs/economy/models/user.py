class User:
    def __init__(self,
                 id:int,
                 username:str,
                 xp:int = 0,
                 coins:int = 0):
        self.id = id
        self.xp = xp
        self.coins = coins
        self.username = username
