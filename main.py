import telebot
import time

TELEBOT_TOKEN_ID = "6463635955:AAE1FVJf36OefFbxUwAM0XBKmn0HGCw0qvc"

tele_bot = telebot.TeleBot(TELEBOT_TOKEN_ID)


@tele_bot.message_handler(commands=['chat_id'])
def chat_id_request(message):
    tele_bot.send_message(message.chat.id, f"Current chat id is {message.chat.id}")


# @tele_bot.message_handler()
# def msg_request(message):
#     ii = 0


if __name__ == '__main__':
    while True:
        time.sleep(10)