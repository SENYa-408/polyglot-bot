import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
# from telegram.ext import Updater, CommandHandler, PollHandler, MessageHandler, Filters
# import poll

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Hey! I'm Julius the polyglot and I'll help you learn your new language! \n\n /help for more info")

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.reply("Help info: \n I support all languages that wordreference.com does \n\n Type the word of the learning language to add it to your wordlist \n /quiz - answer a quiz for a random word! (wordlist in priority) \n /wordlist - shows your wordlist \n /delete *word* - deletes *word* from your wordlist")

@dp.message_handler(commands=["quiz"])
async def quiz(message: types.Message):
    await message.reply("In work")

@dp.message_handler(commands=["wordlist"])
async def wordlist(message: types.Message):
    await message.reply("In work")

@dp.message_handler(commands=["delete"])
async def delete(message: types.Message):
    await message.reply("In work")

@dp.message_handler()
async def word(message: types.Message):
    await message.reply("In work")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)