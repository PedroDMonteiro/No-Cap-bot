import os
from typing import Sequence
from utils.erros.database import *

import mariadb
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("DATABASE_PASSWORD")

class Database():
    def __get_connection(self):
        return mariadb.connect(user="root",
                               password=PASSWORD,
                               host="localhost",
                               port=3306,
                               database=DATABASE,
                               )

    def __execute(self, cursor: mariadb.cursors.Cursor, sql: str, args: Sequence):
        try:
            cursor.execute(sql,args)
        except Exception as err:
            custom_err = err
            str_err = str(err).upper()
            print(err)
            if isinstance(err,mariadb.ProgrammingError):
                raise err
                # raise Syntax_Error(f'{err}')
            
            if isinstance(err,mariadb.IntegrityError):
                if str_err.startswith("DUPLICATE"):
                    raise Primary_Key_Duplicate()
            
            if isinstance(err,mariadb.DataError):
                pass
        
            raise custom_err

    def create(self, sql:str, args: Sequence = ()):
        try:
            con = self.__get_connection()
            cur = con.cursor()
            self.__execute(cur,sql,args)
            con.commit()
            con.close()
        except Exception as err:
            con.rollback()
            con.close()
            raise(err)

    def select_one(self, sql:str, args: Sequence = ()):
        try:
            con = self.__get_connection()
            cur = con.cursor()
            self.__execute(cur,sql,args)
            # con.commit()
            row = cur.fetchone()
            con.close()

            return row
        except Exception as err:
            # con.rollback()
            con.close()
            raise(err)

    def select_all(self, sql:str, args: Sequence = ()):
        try:
            con = self.__get_connection()
            cur = con.cursor()
            self.__execute(cur,sql,args)
            # con.commit()
            rows = cur.fetchall()
            con.close()

            return rows
        except Exception as err:
            con.close()
            raise(err)

    def update(self, sql:str, args: Sequence = ()):
        try:
            con = self.__get_connection()
            cur = con.cursor()
            self.__execute(cur,sql,args)
            con.commit()
            con.close()
        except Exception as err:
            con.rollback()
            con.close()
            raise(err)

    def delete(self, sql:str, args: Sequence = ()):
        try:
            con = self.__get_connection()
            cur = con.cursor()
            self.__execute(cur,sql,args)
            con.commit()
            con.close()
        except Exception as err:
            con.rollback()
            con.close()
            raise(err)