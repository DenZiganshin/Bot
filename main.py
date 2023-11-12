import telebot
import time

TELEBOT_TOKEN_ID = "6463635955:AAE1FVJf36OefFbxUwAM0XBKmn0HGCw0qvc"

tele_bot = telebot.TeleBot(TELEBOT_TOKEN_ID)


# полинг сообщений "/chat_id"
@tele_bot.message_handler(commands=['chat_id'])
def chat_id_request(message):
    tele_bot.send_message(message.chat.id, f"Current chat id is {message.chat.id}")


# полинг всех сообщение
@tele_bot.message_handler()
def msg_request(message):
    tele_bot.send_message(message.chat.id, f"Last message from {message.from_user.full_name}  ({message.from_user.username}): {message.html_text}")
    if message.from_user.is_bot:
        tele_bot.send_message(message.chat.id, f"This is bot")
    else:
        tele_bot.send_message(message.chat.id, f"This not is bot")


if __name__ == '__main__':
    tele_bot.infinity_polling()
