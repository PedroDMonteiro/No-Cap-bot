class DB_error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
         return f"{self.message}"

class Unkown_Error(Exception):
    def __init__(self):
        pass

class Primary_Key_Duplicate(Exception):
    def __init__(self):
        pass

class Syntax_Error(Exception):
    def __init__(self):
        pass

class Programming_Error(Exception):
    def __init__(self):
        pass

class Integrity_Error(Exception):
    def __init__(self):
        pass

class Data_Error(Exception):
    def __init__(self):
        pass

class Custom_Exception(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Already_Vote(Custom_Exception):
    def __init__(self, *args):
        super().__init__(*args)

class User_Not_Found(Exception):
    def __init__(self,identifier):
        self.identifier = identifier
        super().__init__()

    def __str__(self):
        return f"`{self.identifier}` não cadastrado"
    
class Table_Not_Found(Custom_Exception):
    def __init__(self, table):
        self.table = table
        super().__init__()

    def __str__(self):
        return f"`{self.table}` not found"