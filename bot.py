import telebot
import logging
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.DEBUG)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name

if __name__ == "__main__":
    logging.info("Бот запускается")
    bot.polling()