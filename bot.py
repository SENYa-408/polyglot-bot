import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

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
    res = "Help info: \n\n Type the word of the learning language to add it to your wordlist \n /quiz - answer a quiz for a random word! (wordlist in priority) \n /wordlist - shows your wordlist \n /delete *word* - deletes *word* from your wordlist \n /dictionaries - check all dictionraies that i support \n /set - set your dictionary"
    await message.reply(res)

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
    res = "In work"
    await message.reply(res)

@dp.message_handler(commands=["delete"])
async def delete(message: types.Message):
    res = "In work"
    await message.reply(res)

@dp.message_handler(commands=["dictionaries"])
async def dictionaries(message: types.Message):
    dicts = wr.get_dicts()

    res = ""
    for el in dicts:
        res += "(" + el + ") " + dicts[el]['from'] + " => " + dicts[el]['to'] + "\n"

    await message.reply(res)

@dp.message_handler(commands=["set"])
async def set(message: types.Message):
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
async def word(message: types.Message):
    user_id = message.from_user.id
    word = message.text

    db.add_word_to_wordlist(user_id, word)

    res = f"Added *{word}* to your wordlist"
    await message.reply(res)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)