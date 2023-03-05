# **dizi-polyglot-bot :earth_africa:**

:warning: PROJECT IN THE DEVELOPMENT STATE :warning:

Telegram bot to help you improve your vocabulary   
**Created with** [aiogram](https://github.com/aiogram/aiogram)

# Discription
Bot is designed to help users learn new vocabulary by collecting user-defined words and creating quizzes with further explanation by providing instant view article from [wordreference.com](https://www.wordreference.com/).

### Existing solutions
- [MemcardsBot](https://t.me/memorizationbot) [[Source](https://github.com/bouk/memorizationbot)] - Bot written in Go that reminds you to answer your flashcards and asks how well they were answered.
- [MyFlashcardsBot](https://t.me/MyFlashcardsBot) - Bot currenltly under maintence.

### Differences
- Don't have quiz option for practicing
- Not focused on language learning
- Currently not available for use.

### Telegram
- No need to download application for the user
- More convinient to use as it is the part of the Telegram application
- Easier development as there is no need to think about notification, iterface implementation and so on

# Usage
:warning:CURRENTLY OFF:warning:
- Find **@dizi-polyglot-bot** in telegram search
- Click **Start**

# Command list
`/start` - start the bot  
`/help` - help info  

`/quiz` - create the quiz  
`/wordlist` - show the wordlist  
`/delete word` - delete `word` from the wordlist  
`/dictionaries` - check all supported dictionraies with their codes   
`/set iten` - set user dictionary to `iten` (Italian-English)  
`word` - adds `word` to the wordlist  

# Install
1. Clone git repository 
 
   `git clone https://github.com/SENYa-408/dizi-polyglot-bot.git`
2. Go to directory with project  
3. Download all dependencies  

   `pip install aiogram python-dotenv`  
4. Set environment variables in `.env` file in the root directory ([see example](/.env.example))  

   | Variable       | Usage                                                       |
   | -------------- | ------------------------------------------------------------|
   | TOKEN          | Telegram Bot token from [@BotFather](https://t.me/BotFather)|
5. Start bot  
   `python bot.py`
