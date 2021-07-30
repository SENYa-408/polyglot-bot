import os
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

load_dotenv()

token = os.getenv('TOKEN')

updater = Updater(token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

words = []

def start(update, context):
    chat_id = update.effective_chat.id
    
    response = "Hey! \n /help for more info"

    context.bot.send_message(chat_id, response)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(update, context):
    chat_id = update.effective_chat.id
    
    response = "help info"

    context.bot.send_message(chat_id, response)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def wordlist(update, context):
    chat_id = update.effective_chat.id
    
    if not words:
        response = 'you have no words'
    else: 
        response = '\n'.join(words)

    context.bot.send_message(chat_id, response)

wordlist_handler = CommandHandler('wordlist', wordlist)
dispatcher.add_handler(wordlist_handler)

def echo(update, context):
    chat_id = update.effective_chat.id

    response = update.message.text

    if(not (update.message.text.lower() in words)):
        words.append(update.message.text.lower())

    context.bot.send_message(chat_id, response)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()