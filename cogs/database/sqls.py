from database.general import Database as db
from utils.erros.database import Table_Not_Found
from myBot import MyBot

async def setup(bot: MyBot):
    pass

class Database(db):
    def table_exist(self, table: str) -> bool:
        query = ""
        query += "\n" + f"SELECT *"
        query += "\n" + f"FROM information_schema.tables"
        query += "\n" + f"WHERE table_schema = 'no cap'"
        query += "\n" + f"AND TABLE_NAME = '{table}'"
        rows = self.select_all(query)

        return len(rows) > 0
    
    def get_columns(self, table: str) -> list[str]:
        if not Database.table_exist(table):
            raise Table_Not_Found(table)
        
        query = ""
        query += "\n" + f"SELECT COLUMN_NAME"
        query += "\n" + f"FROM information_schema.columns"
        query += "\n" + f"WHERE table_schema = 'no cap'"
        query += "\n" + f"AND TABLE_NAME = '{table}'"
        rows = self.select_all(query)

        return [row[0] for row in rows]
    
    def table(self, table) -> tuple[list[str],list[any]]:
        columns = self.get_columns(table)

        query = ""
        query += "\n" + f"SELECT {','.join(columns)}"
        query += "\n" + f"FROM {table}"
        rows = self.select_all(query)

        return columns,rows
    