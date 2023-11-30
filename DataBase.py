import sqlite3
from pathlib import Path


class DataBase:
    def __init__(self, db_path=Path('~').expanduser() / ".balabol_bot/database.db"):
        self.__open_db(db_path)

    def __open_db(self, db_path):
        self.connection = sqlite3.connect(str(db_path), check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.commit()
        self.connection.close()
