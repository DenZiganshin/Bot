import sqlite3
from pathlib import Path


class DataBase:
    def __init__(self, db_path=Path('~').expanduser() / ".balabol_bot/database.db"):
        self.__connection = sqlite3.connect(str(db_path))
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS Phrase_value (
        id INTEGER PRIMARY KEY,
        chat INTEGER NOT NULL,
        message TEXT NOT NULL
        )
        ''')

    def get_messages(self, chat_id):
        self.__cursor.execute('SELECT message FROM Phrase_value where chat = ?', (chat_id, ))
        return self.__cursor.fetchall()

    def get_rand_id(self, chat_id, count):
        self.__cursor.execute('SELECT id FROM Phrase_value where chat = ? ORDER BY RANDOM() LIMIT ?',
                              (chat_id, count,))
        return self.__cursor.fetchall()

    def remove(self, id):
        self.__cursor.execute('DELETE FROM Phrase_value WHERE id = ? ',
                              (id,))

    def add_messages(self, chat_id, message):
        self.__cursor.execute('INSERT INTO Phrase_value (chat, message) VALUES (?, ?)',
                       (chat_id, message))
        self.__connection.commit()

    def clear(self):
        self.__cursor.execute('DELETE FROM Phrase_value')
        self.__connection.commit()

    def __del__(self):
        self.__connection.commit()
        self.__connection.close()


if __name__ == '__main__':
    db = DataBase("tests/config/database.db")

    db.add_messages(1, "a1")
    db.add_messages(1, "a2")
    db.add_messages(1, "a3")
    db.add_messages(1, "a4")

    db.add_messages(2, "a1")
    db.add_messages(2, "a2")
    db.add_messages(2, "a3")
    db.add_messages(2, "a4")

    res = db.get_messages(1)
    res_rend = db.get_rand_id(1, 1)

    for id_tuple in res_rend:
        id = id_tuple[0]
        db.remove(id)

    res2 = db.get_messages(1)

    db.clear()

    res3 = db.get_messages(1)

    print(f"res {res}")
    print(f"res_rend {res_rend}")
    print(f"res2 {res2}")
    print(f"res3 {res3}")

