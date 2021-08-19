import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, PollHandler, MessageHandler, Filters
import logging
import poll_controller
load_dotenv()

token = os.getenv('TOKEN')

updater = Updater(token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
    
    if not poll_controller.user_wordlist:
        response = 'Your wordlist is empty :( \n Type the word of the learning language to add it to your wordlist '
    else: 
        response = '\n'.join(poll_controller.user_wordlist)

    context.bot.send_message(chat_id, response)

wordlist_handler = CommandHandler('wordlist', wordlist)
dispatcher.add_handler(wordlist_handler)

def test(update, context):
    chat_id = update.effective_chat.id
    
    word, options, correct_option_id = poll_controller.create_options()

    context.bot.send_poll(chat_id, word, options, True, 'quiz', False, correct_option_id)

test_handler = CommandHandler('test', test)
dispatcher.add_handler(test_handler)

def learned(update, context):
    options = update.poll.options
    correct_option_id = update.poll.correct_option_id

    counter = 0
    answer = False

    for option in options:
        if option.voter_count == 1 and correct_option_id == counter:
            answer = option.text
            break
            
        counter += 1

    if answer:
        poll_controller.user_learned_words.append(answer)

    if answer in poll_controller.user_wordlist:
        poll_controller.user_wordlist.remove(answer)

learned_handler = PollHandler(learned, pass_chat_data=True, pass_user_data=True)
dispatcher.add_handler(learned_handler)

def delete(update, context):
    chat_id = update.effective_chat.id

    message_text = update.message.text.split(' ')

    word = message_text[1] if len(message_text) >= 2 else ''

    if(word.lower() in poll_controller.user_wordlist):
        poll_controller.user_wordlist.remove(word.lower())
        response = 'The word has been successfully deleted!'
    else:
        response = 'there\'s no ' + word + ' in the /wordlist \n example: \'/delete house\''

    context.bot.send_message(chat_id, response)

delete_handler = CommandHandler('delete', delete)
dispatcher.add_handler(delete_handler)

def echo(update, context):
    chat_id = update.effective_chat.id

    response = update.message.text

    if(update.message.text.lower() in poll_controller.user_wordlist):
        response = 'ERROR: word is already in the list'
    elif(not(poll_controller.get_synonyms(update.message.text.lower()))):
        response = 'ERROR: there\'s no ' + update.message.text + ' in the dictionary'
    else:
        poll_controller.user_wordlist.append(update.message.text.lower())

    context.bot.send_message(chat_id, response)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()