import telebot
import random
import math

from BotConfig import BotConfig
from DataBase import DataBase
from PhrasesTable import PhrasesTable
from ConfigTable import ConfigTable
from SystemRegistryTable import SystemRegistryTable


bot_config = BotConfig()
tele_bot = telebot.TeleBot(bot_config.telebot_token_id)

bot_data_base = DataBase()
bot_message_base = PhrasesTable(bot_data_base)
bot_config_base = ConfigTable(bot_data_base)
bot_system_registration_base = SystemRegistryTable(bot_data_base)


@tele_bot.message_handler(commands=['show_for_me_this_fucking_config'])
def chat_id_request(message):
    tele_bot.send_message(message.chat.id, f"database_row_limit: {bot_config_base.get_database_row_limit(message.chat.id)}\n"
                                           f"phrases_in_bot_message_count: {bot_config_base.get_phrases_in_bot_message_count(message.chat.id)}\n"
                                           f"inbound_phrase_length_limit: {bot_config_base.get_inbound_phrase_length_limit(message.chat.id)}\n"
                                           f"message_initiation_frequency: {bot_config_base.get_message_initiation_frequency(message.chat.id)}")


@tele_bot.message_handler(commands=['help'])
def help_request(message):
    tele_bot.send_message(message.chat.id, f"/chat_id - current chat ID\n"
                                           f"/show_for_me_this_fucking_config - config for current chat\n"
                                           f"/debug_message_database - file with messages from data base\n"
                                           f"/set_database_row_limit - update database row limit\n"
                                           f"/set_phrases_in_bot_message_count - update phrases in bot message count\n"
                                           f"/set_inbound_phrase_length_limit - update inbound phrase length limit\n"
                                           f"/set_message_initiation_frequency - update message initiation frequency")


# полинг сообщений "/chat_id"
@tele_bot.message_handler(commands=['chat_id'])
def chat_id_request(message):
    tele_bot.send_message(message.chat.id, f"Current chat id is {message.chat.id}")


# полинг сообщений "/debug_message_database"
@tele_bot.message_handler(commands=['debug_message_database'])
def chat_id_request(message):
    messages = bot_message_base.get_messages(message.chat.id)
    if len(messages) == 0:
        tele_bot.send_message(message.chat.id, "No data")
    else:
        debug_messages_file = open('debug_messages.txt', 'w+')
        for line in messages:
            debug_messages_file.write(f"{line[0]}\n")
        debug_messages_file.seek(0)

        tele_bot.send_document(message.chat.id, debug_messages_file)


def erase_name(name, msg):
    return msg.replace(f"/{name} ", '')


def get_msg_frequency(chat_id):
    return (bot_config_base.get_message_initiation_frequency(chat_id) /
            math.pow(2.0, bot_system_registration_base.get_bot_serial_msg_cnt(chat_id)))


@tele_bot.message_handler(commands=['set_database_row_limit'], content_types=['text'])
def set_database_row_limit_handler(message):
    text = erase_name("set_database_row_limit", message.text)
    if text is not None:
        try:
            value = int(text)
            if 1 <= value <= 500:
                bot_config_base.set_database_row_limit(message.chat.id, value)
            else:
                tele_bot.send_message(message.chat.id, f"Invalid value")
        except ValueError:
            tele_bot.send_message(message.chat.id, f"Invalid value")
            return
    else:
        tele_bot.send_message(message.chat.id, f"Empty data")


@tele_bot.message_handler(commands=['set_phrases_in_bot_message_count'], content_types=['text'])
def set_database_row_limit_handler(message):
    text = erase_name("set_phrases_in_bot_message_count", message.text)
    if text is not None:
        try:
            value = int(text)
            if 0 <= value <= 10:
                bot_config_base.set_phrases_in_bot_message_count(message.chat.id, value)
            else:
                tele_bot.send_message(message.chat.id, f"Invalid value")
        except ValueError:
            tele_bot.send_message(message.chat.id, f"Invalid value")
            return
    else:
        tele_bot.send_message(message.chat.id, f"Empty data")


@tele_bot.message_handler(commands=['set_inbound_phrase_length_limit'], content_types=['text'])
def set_database_row_limit_handler(message):
    text = erase_name("set_inbound_phrase_length_limit", message.text)
    if text is not None:
        try:
            value = int(text)
            if 0 <= value <= 100:
                bot_config_base.set_inbound_phrase_length_limit(message.chat.id, value)
            else:
                tele_bot.send_message(message.chat.id, f"Invalid value")
        except ValueError:
            tele_bot.send_message(message.chat.id, f"Invalid value")
            return
    else:
        tele_bot.send_message(message.chat.id, f"Empty data")


@tele_bot.message_handler(commands=['set_message_initiation_frequency'], content_types=['text'])
def set_database_row_limit_handler(message):
    text = erase_name("set_message_initiation_frequency", message.text)
    if text is not None:
        try:
            value = int(text)
            if 0 <= value <= 100:
                bot_config_base.set_message_initiation_frequency(message.chat.id, value)
            else:
                tele_bot.send_message(message.chat.id, f"Invalid value")
        except ValueError:
            tele_bot.send_message(message.chat.id, f"Invalid value")
            return
    else:
        tele_bot.send_message(message.chat.id, f"Empty data")


# полинг всех сообщение
@tele_bot.message_handler()
def msg_request(message):

    # пропуск сообщений от ботов
    if message.from_user.is_bot:
        return

    if not bot_message_base.is_text_contains_link(message.html_text):
        phrases = bot_message_base.parse_phrases(message.html_text)
        bot_message_base.insert_new_data(message.chat.id, phrases, bot_config_base.get_database_row_limit(message.chat.id))
    
    # make some response
    random_num = random.randint(0, 100)
    if random_num <= get_msg_frequency(message.chat.id):
        phrase_cnt = bot_config_base.get_phrases_in_bot_message_count(message.chat.id)
        if phrase_cnt > 0:
            phrase_postfixes = ["!", ".", "?"]
            response_text = ""
            phrases = bot_message_base.get_rand_messages(message.chat.id, phrase_cnt)
            for ph in phrases:
                if response_text:
                    response_text += " "
                response_text += ph
                response_text += phrase_postfixes[random.randint(0, len(phrase_postfixes) - 1)]
            if response_text:
                tele_bot.send_message(message.chat.id, response_text)

                # update count of serial msg from bot
                bot_system_registration_base.increment_bot_serial_msg_cnt(message.chat.id)
                return

    # reset serial messages
    bot_system_registration_base.reset_bot_serial_msg_cnt(message.chat.id)


if __name__ == '__main__':
    random.seed()
    tele_bot.infinity_polling()
