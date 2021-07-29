import os
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
words = ['hhh','ppp','kkk']

bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(msg):
	bot.send_message(msg.chat.id, 'Hey! I\'ll help you improve your vocabulary. \n/help for more info')

@bot.message_handler(commands=['help'])
def send_help(msg):
	bot.send_message(msg.chat.id, 'help info')

@bot.message_handler(commands=['wordlist'])
def send_help(msg):
	response = '\n'.join(words)

	bot.send_message(msg.chat.id, response)

@bot.message_handler(func=lambda m: True)
def echo_all(msg):
	if(not (msg.text.lower() in words)):
		words.append(msg.text.lower())

	bot.send_message(msg.chat.id, msg.text)

bot.polling()