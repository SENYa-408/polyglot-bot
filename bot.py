import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode

from db import db_controller as db
from api import wordreference as wr

db.init()

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id

    db.add_user(user_id)

    res = "Hey! I'm Dizi the polyglot and I'll help you learn your new language! \n\n /help for more info"
    await message.reply(res)

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    res = "*Help info:* \n\n Type the word of the learning language to add it to your wordlist \n /quiz - answer a quiz for a random word! (wordlist in priority) \n /wordlist - shows your wordlist \n /delete *word* - deletes *word* from your wordlist \n /dictionaries - check all dictionraies that i support \n /set - set your dictionary"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["quiz"])
async def quiz(message: types.Message):
    question = "Your answer?"
    options = ["A", "B", "C", "D"]
    explanation = "The right answer is C"
    await message.answer_poll(
        question=question,
        options=options,
        type="quiz",
        correct_option_id=2,
        is_anonymous=True,
        explanation=explanation
    )

@dp.message_handler(commands=["wordlist"])
async def wordlist(message: types.Message):
    user_id = message.from_user.id

    words = db.get_all_words(user_id)

    learned_words_num = len(db.get_all_learned_words(user_id))
    words_num = len(words)
    
    res = f"*Learned words: {learned_words_num} \nWordlist size: {words_num}* \n"
    for word in words:
        res += word + "\n"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["delete"])
async def delete(message: types.Message):
    user_id = message.from_user.id
    word = message.get_args()

    db.remove_word_from_wordlist(user_id, word)

    res = f"Removed *{word}* from your wordlist"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["dictionaries"])
async def dictionaries(message: types.Message):
    dicts = wr.get_dicts()

    res = "*Here's all languages I support:* \n"
    for el in dicts:
        res += "[[" + el[:2] + "]] " + dicts[el]['from'] + "\n"

    await message.reply(res, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["set"])
async def set(message: types.Message):
    user_id = message.from_user.id
    dict_lang = message.get_args()
    is_dict_correct = wr.check_dict(dict_lang)

    if is_dict_correct:
        db.update_user_dict(user_id, dict_lang + 'en')
        res = f"Dictionary {dict_lang} selected"
    else:
        res = "This dictionary doesn't exist, see /dictionaries" 

    await message.reply(res)

@dp.message_handler()
async def word(message: types.Message):
    user_id = message.from_user.id
    word = message.text

    dict_code = db.get_dict_code(user_id)
    is_word_correct = wr.get_translation(dict_code, word)

    if is_word_correct:
        db.add_word_to_wordlist(user_id, word)
        res = f"Added *{word}* to your wordlist"
    else:
        res = f"There's no *{word}* in the dictionary"
    await message.reply(res, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)