import telebot
from BotConfig import BotConfig
from DataBase import DataBase
from PhrasesTable import PhrasesTable


bot_config = BotConfig()
tele_bot = telebot.TeleBot(bot_config.telebot_token_id)

bot_data_base = DataBase()
bot_message_base = PhrasesTable(bot_data_base, bot_config.database_row_limit)


@tele_bot.message_handler(commands=['show_for_me_this_fucking_config'])
def chat_id_request(message):
    tele_bot.send_message(message.chat.id, f"database_row_limit: {bot_config.database_row_limit}\n"
                                           f"phrases_in_bot_message_count: {bot_config.phrases_in_bot_message_count}\n"
                                           f"inbound_phrase_length_limit: {bot_config.inbound_phrase_length_limit}\n"
                                           f"message_initiation_frequency: {bot_config.message_initiation_frequency}")


# полинг сообщений "/chat_id"
@tele_bot.message_handler(commands=['chat_id'])
def chat_id_request(message):
    tele_bot.send_message(message.chat.id, f"Current chat id is {message.chat.id}")


# полинг всех сообщение
@tele_bot.message_handler()
def msg_request(message):
    tele_bot.send_message(message.chat.id,
                          f"Last message from {message.from_user.full_name}  ({message.from_user.username}): "
                          f"{message.html_text}")
    if message.from_user.is_bot:
        tele_bot.send_message(message.chat.id, f"This is bot")
    else:
        tele_bot.send_message(message.chat.id, f"This not is bot")


if __name__ == '__main__':
    tele_bot.infinity_polling()
