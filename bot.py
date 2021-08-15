import os
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import random
from googletrans import Translator 
from nltk.corpus import wordnet

load_dotenv()

token = os.getenv('TOKEN')

updater = Updater(token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

translator = Translator()

words = []

def get_synonyms(word):

    if(not isinstance(word, str)):
        return False

    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() not in synonyms and l.name() != word and not '_' in l.name():
                synonyms.append(l.name())

    return synonyms

def start(update, context):
    chat_id = update.effective_chat.id
    
    response = "Hey! I'm a polyglot bot and I'll help you remember new words :) \n test yourself whenever you want! \n /help for more info"

    context.bot.send_message(chat_id, response)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(update, context):
    chat_id = update.effective_chat.id
    
    response = "Help info: \n Current supported languages: \n ru -> en \n\n Type the word of the learning language to add it to your wordlist \n /wordlist - check your wordlist \n /test - test random word from your wordlist \n /delete *word* - delete word form your wordlist"

    context.bot.send_message(chat_id, response)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def wordlist(update, context):
    chat_id = update.effective_chat.id
    
    if not words:
        response = 'Your wordlist is empty :( \n Type the word of the learning language to add it to your wordlist '
    else: 
        response = '\n'.join(words)

    context.bot.send_message(chat_id, response)

wordlist_handler = CommandHandler('wordlist', wordlist)
dispatcher.add_handler(wordlist_handler)

def test(update, context):
    chat_id = update.effective_chat.id
    
    word = random.choice(words)

    options = get_synonyms(word)
    del options[2:]

    options.append(word)

    random.shuffle(options)

    correct_option_id = options.index(word)

    for index, option in enumerate(options):
        options[index] = translator.translate(option, dest='ru').text

    context.bot.send_poll(chat_id, word, options, True, 'quiz', False, correct_option_id)

test_handler = CommandHandler('test', test)
dispatcher.add_handler(test_handler)

def delete(update, context):
    chat_id = update.effective_chat.id

    message_text = update.message.text.split(' ')

    word = message_text[1] if len(message_text) >= 2 else ''

    if(word.lower() in words):
        words.remove(word.lower())
        response = 'The word has been successfully deleted!'
    else:
        response = 'there\'s no ' + word + ' in the /wordlist \n example: \'/delete house\''

    context.bot.send_message(chat_id, response)

delete_handler = CommandHandler('delete', delete)
dispatcher.add_handler(delete_handler)

def echo(update, context):
    chat_id = update.effective_chat.id

    response = update.message.text

    if(update.message.text.lower() in words):
        response = 'ERROR: word is already in the list'
    elif(not(get_synonyms(update.message.text.lower()))):
        response = 'ERROR: there\'s no ' + update.message.text + ' in the dictionary'
    else:
        words.append(update.message.text.lower())

    context.bot.send_message(chat_id, response)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()