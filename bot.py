import os
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ParseMode, Message, PollAnswer

from db import db_controller as db
from api import wordreference as wr

db.init()

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: Message):
    user_id = message.from_user.id

    db.add_user(user_id)

    res = "Hey! I'm Dizi the polyglot and I'll help you learn your new language! \n\n /help for more info"
    await message.reply(res)

@dp.message_handler(commands=["help"])
async def help(message: Message):
    res = "*Help info:* \n\n Type the word of the learning language to add it to your wordlist \n /quiz - answer a quiz for a random word! (wordlist in priority) \n /wordlist - shows your wordlist \n /delete *word* - deletes *word* from your wordlist \n /dictionaries - check all dictionraies that i support \n /set - set your dictionary"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["quiz"])
async def quiz(message: Message):
    user_id = message.from_user.id

    words = db.get_random_words(user_id, 4)

    if len(words) < 4:
        res = "Your wordlist must be at least 4 words long, see /help"

        return await message.reply(res)

    correct_option_id = random.randint(0, 3)
    question = words[correct_option_id]
    quiz.question = question

    user_dict_code = db.get_dict_code(user_id)
    translations = wr.get_translation(user_dict_code, words)

    options = translations

    await message.answer_poll(
        question=question,
        options=options,
        type="quiz",
        correct_option_id=correct_option_id,
        is_anonymous=False
    )

@dp.poll_answer_handler()
async def quiz_answer(poll_answer: PollAnswer):
    user_id = poll_answer.user.id
    user_dict_code = db.get_dict_code(user_id)
    word = quiz.question

    res = f"Read more:\nhttps://www.wordreference.com/{user_dict_code}en/{word}"
    await bot.send_message(user_id, res)

@dp.message_handler(commands=["wordlist"])
async def wordlist(message: Message):
    user_id = message.from_user.id

    words = db.get_all_user_words(user_id)

    learned_words_num = len(db.get_all_user_learned_words(user_id))
    words_num = len(words)
    
    res = f"*Learned words: {learned_words_num} \nWordlist size: {words_num}* \n"
    for word in words:
        res += word + "\n"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["delete"])
async def delete(message: Message):
    user_id = message.from_user.id
    word = message.get_args()

    db.remove_word_from_wordlist(user_id, word)

    res = f"Removed *{word}* from your wordlist"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["dictionaries"])
async def dictionaries(message: Message):
    dicts = wr.get_dicts()

    res = "*Here's all languages I support:* \n"
    for el in dicts:
        res += "[[" + el[:2] + "]] " + dicts[el]['from'] + "\n"

    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["set"])
async def set(message: Message):
    user_id = message.from_user.id
    dict_lang = message.get_args()
    is_dict_correct = wr.check_dict(dict_lang)

    if is_dict_correct:
        db.update_user_dict(user_id, dict_lang)
        res = f"Dictionary {dict_lang} selected"
    else:
        res = "This dictionary doesn't exist, see /dictionaries" 

    await message.reply(res)

@dp.message_handler()
async def word(message: Message):
    user_id = message.from_user.id
    word = message.text

    dict_code = db.get_dict_code(user_id)

    if dict_code:
        is_word_correct = wr.get_translation(dict_code, [word,])

        if is_word_correct:
            db.add_word_to_wordlist(user_id, word)
            res = f"Added *{word}* to your wordlist"
        else:
            res = f"There's no *{word}* in the dictionary"
    else:
        res = "Please select your dictionary first, see /help"

    await message.reply(res, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)