import DataBaseBase

class DataBase:
    def __init__(self, max_chat_data_count, database:DataBaseBase):
        self.__data_base = database
        self.__table_name = "Phrase_value"
        self.__max_chat_data_count = max_chat_data_count
        self.__open_table()

    def get_rand_messages(self, chat_id, count):
        res_rand = self.__get_rand_id(chat_id, count)

        messages = []
        for id_tuple in res_rand:
            messages.append(self.__get_message(id_tuple[0])[0])
        return messages

    def insert_new_data(self, chat_id, messages):
        messages = self.__remove_not_unique(messages)
        messages = self.__remove_existed(chat_id, messages)
        self.__remove_oversize(chat_id, messages)

        for msg in messages:
            self.__add_messages(chat_id, msg)

    def get_messages(self, chat_id):
        self.__data_base.cursor.execute(f'SELECT message FROM {self.__table_name} where chat = ?', (chat_id, ))
        return self.__data_base.cursor.fetchall()

    def remove(self, id):
        self.__data_base.cursor.execute(f'DELETE FROM {self.__table_name} WHERE id = ? ',
                              (id,))

    def clear(self):
        self.__data_base.cursor.execute(f'DELETE FROM {self.__table_name}')
        self.__data_base.connection.commit()

    def __open_table(self):
        self.__data_base.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.__table_name} (
                id INTEGER PRIMARY KEY,
                chat INTEGER NOT NULL,
                message TEXT NOT NULL
                )
                ''')

    def __get_message(self, id):
        self.__data_base.cursor.execute(f'SELECT message FROM {self.__table_name} where id = ?', (id, ))
        msg_list = self.__data_base.cursor.fetchall()
        if len(msg_list) == 0:
            return None
        else:
            return msg_list[0]

    @staticmethod
    def __remove_not_unique(messages):
        return list(set(messages))

    def __remove_existed(self, chat_id, message):
        res_msgs = []
        for msg in message:
            if not self.__is_message_exists(chat_id, msg):
                res_msgs.append(msg)
        return res_msgs

    def __is_message_exists(self, chat_id, messages):
        self.__data_base.cursor.execute(f'SELECT message FROM {self.__table_name} where chat = ? and message = ?',
                              (chat_id, messages))
        return len(self.__data_base.cursor.fetchall()) != 0

    def __add_messages(self, chat_id, message):
        self.__data_base.cursor.execute(f'INSERT INTO {self.__table_name} (chat, message) VALUES (?, ?)',
                       (chat_id, message))
        self.__data_base.connection.commit()

    def __get_rand_id(self, chat_id, count):
        self.__data_base.cursor.execute(f'SELECT id FROM {self.__table_name} where chat = ? ORDER BY RANDOM() LIMIT ?',
                              (chat_id, count,))
        return self.__data_base.cursor.fetchall()

    def __remove_oversize(self, chat_id, messages):
        cnt_for_remove = len(messages) + len(self.get_messages(chat_id)) - self.__max_chat_data_count
        if cnt_for_remove > 0:
            ids = self.__get_rand_id(chat_id, cnt_for_remove)
            for id_for_remove in ids:
                self.remove(id_for_remove[0])


if __name__ == '__main__':
    db_base = DataBaseBase.DataBaseBase("tests/config/database.db")

    db = DataBase(2, db_base)

    db.insert_new_data(1, {"a1"})
    db.insert_new_data(1, {"a2"})
    db.insert_new_data(1, {"a3"})
    db.insert_new_data(1, {"a4"})

    db.insert_new_data(2, {"a1"})
    db.insert_new_data(2, {"a2"})
    db.insert_new_data(2, {"a3"})
    db.insert_new_data(2, {"a4"})

    res = db.get_messages(1)
    res_rend = db.get_rand_messages(1, 1)

    for id_tuple in res_rend:
        db.remove(id_tuple[0])

    res2 = db.get_messages(1)

    msgs = db.get_rand_messages(1, 1)

    db.clear()

    res3 = db.get_messages(1)

    print(f"res {res}")
    print(f"res_rend {res_rend}")
    print(f"res2 {res2}")
    print(f"res3 {res3}")

