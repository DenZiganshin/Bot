import sqlite3
from pathlib import Path

class DataBase:
    def __init__(self, db_path=Path('~').expanduser() / ".balabol_bot/database.db"):
        self.__connection = sqlite3.connect(str(db_path))
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
        id INTEGER PRIMARY KEY,
        chat INTEGER NOT NULL,
        message TEXT NOT NULL
        )
        ''')

    def get_messages(self, chat_id):
        self.__cursor.execute('SELECT message FROM Messages where chat = ?', (chat_id, ))
        return self.__cursor.fetchall()

    def add_messages(self, chat_id, message):
        self.__cursor.execute('INSERT INTO Messages (chat, message) VALUES (?, ?)',
                       (chat_id, message))
        self.__connection.commit()

    def __del__(self):
        self.__connection.commit()
        self.__connection.close()


if __name__ == '__main__':
    db = DataBase()
    # db.add_messages(1, "123")
    res = db.get_messages(1)
    i = 0
