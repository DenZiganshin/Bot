import datetime
from DataBase import DataBase

class ConfigTable:
    def __init__(self, database:DataBase):
        self.__data_base = database
        self.__table_name = "Chat_config"
        self.__open_table()

    def update_time(self, chat_id):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
        else:
            self.__update_value(chat_id, "update_time", datetime.datetime.now())

    def get_update_time(self, chat_id):
        config = self.__get_chat_params(chat_id)
        if config is None:
            return None
        else:
            return datetime.datetime.strptime(config[1], "%Y-%m-%d %H:%M:%S.%f")

    def set_database_row_limit(self, chat_id, value):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
        self.__update_value(chat_id, "database_row_limit", value)

    def get_database_row_limit(self, chat_id):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
            config = self.__get_chat_params(chat_id)
        return config[2]

    def set_phrases_in_bot_message_count (self, chat_id, value):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
        self.__update_value(chat_id, "phrases_in_bot_message_count ", value)

    def get_phrases_in_bot_message_count (self, chat_id):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
            config = self.__get_chat_params(chat_id)
        return config[3]

    def set_inbound_phrase_length_limit(self, chat_id, value):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
        self.__update_value(chat_id, "inbound_phrase_length_limit ", value)

    def get_inbound_phrase_length_limit(self, chat_id):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
            config = self.__get_chat_params(chat_id)
        return config[4]

    def set_message_initiation_frequency(self, chat_id, value):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
        self.__update_value(chat_id, "message_initiation_frequency ", value)

    def get_message_initiation_frequency(self, chat_id):
        config = self.__get_chat_params(chat_id)
        if config is None:
            self.__create(chat_id)
            config = self.__get_chat_params(chat_id)
        return config[5]

    def __open_table(self):
        self.__data_base.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.__table_name} (
                chat_id INTEGER PRIMARY KEY,
                update_time TIMESTAMP,
                database_row_limit INTEGER,
                phrases_in_bot_message_count INTEGER,
                inbound_phrase_lenght_limit INTEGER,
                message_initiation_frequency INTEGER
                )
                ''')
        
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

    def __create(self, chat_id):
        self.__data_base.cursor.execute(f'INSERT INTO {self.__table_name} (chat_id, update_time, database_row_limit, phrases_in_bot_message_count, inbound_phrase_lenght_limit, message_initiation_frequency) VALUES (?, ?, ?, ?, ?, ?)',
                       (chat_id, datetime.datetime.now(), 100, 5, 50, 50))
        self.__data_base.connection.commit()


if __name__ == '__main__':
    db_base = DataBase("tests/config/database.db")

    db = ConfigTable(db_base)

    db.update_time(123)

    res = db.get_update_time(123)

    i = 0