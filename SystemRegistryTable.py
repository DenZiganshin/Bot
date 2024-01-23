from DataBase import DataBase


class SystemRegistryTable:
    def __init__(self, database: DataBase):
        self.__data_base = database
        self.__table_name = "system_registry"
        self.__open_table()

    def __open_table(self):
        self.__data_base.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.__table_name} (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                bot_serial_msg_cnt INTEGER
                )
                ''')

    def __create(self, chat_id):
        self.__data_base.cursor.execute(f'INSERT INTO {self.__table_name} (chat_id, bot_serial_msg_cnt) VALUES (?, ?)',
                       (chat_id, 0))
        self.__data_base.connection.commit()

    def __get_chat_params(self, chat_id):
        self.__data_base.cursor.execute(f'SELECT * FROM {self.__table_name} where chat_id = ?', (chat_id, ))
        msg_list = self.__data_base.cursor.fetchall()
        if len(msg_list) == 0:
            return None
        else:
            return msg_list[0]

    def __update_value(self, chat_id, column_name, value):
        self.__data_base.cursor.execute(f'UPDATE {self.__table_name} set {column_name} = ? where chat_id = ?', (value, chat_id, ))
        self.__data_base.connection.commit()

    def update_bot_serial_msg_cnt(self, chat_id, value: int):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
        self.__update_value(chat_id, "bot_serial_msg_cnt", value)

    def get_bot_serial_msg_cnt(self, chat_id) -> int:
        config = self.__get_chat_params(chat_id)
        if config is None:
            return 0
        else:
            return config[2]

    def increment_bot_serial_msg_cnt(self, chat_id):
        cnt = self.get_bot_serial_msg_cnt(chat_id)
        self.update_bot_serial_msg_cnt(chat_id, cnt + 1)

    def reset_bot_serial_msg_cnt(self, chat_id):
        self.update_bot_serial_msg_cnt(chat_id, 0)


if __name__ == '__main__':
    db_base = DataBase("tests/config/database.db")

    db = SystemRegistryTable(db_base)

    db.update_bot_serial_msg_cnt(123, 100)

    res = db.get_bot_serial_msg_cnt(123)

    db.increment_bot_serial_msg_cnt(123)
    db.increment_bot_serial_msg_cnt(123)
    db.increment_bot_serial_msg_cnt(123)

    res = db.get_bot_serial_msg_cnt(123)

    db.reset_bot_serial_msg_cnt(123)

    res = db.get_bot_serial_msg_cnt(123)

    i = 0