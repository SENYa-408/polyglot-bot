import os
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Hey! I\'ll help you improve your vocabulary. \n/help for more info')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'help info')

bot.polling()