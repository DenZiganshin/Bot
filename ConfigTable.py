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
        # self.__data_base.cursor.execute(f'''
        #         CREATE TABLE IF NOT EXISTS {self.__table_name} (
        #         id INTEGER PRIMARY KEY,
        #         chat INTEGER NOT NULL,
        #         message TEXT NOT NULL
        #         )
        #         ''')
        
    def __get_chat_params(self, chat_id):
        self.__data_base.cursor.execute(f'SELECT * FROM {self.__table_name} where chat_id = ?', (chat_id, ))
        msg_list = self.__data_base.cursor.fetchall()
        if len(msg_list) == 0:
            return None
        else:
            return msg_list[0]
        
    def __update_value(self, chat_id, column_name, value):
        self.__data_base.cursor.execute(f'UPDATE {column_name} FROM {self.__table_name} set {value} where chat_id = ?', (chat_id, ))
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