import sqlite3
from db.tables import create_tables, users, words, user_words, user_learned_words 

def init():
    conn = sqlite3.connect('db/database.db')
    create_tables.init_tables(conn)

# USERS
def add_user(user_id: int):
    conn = sqlite3.connect('db/database.db')
    users.add_user(conn, user_id)

def get_user(user_id: int):
    conn = sqlite3.connect('db/database.db')
    users.get_user(conn, user_id)

def remove_user(user_id: int):
    conn = sqlite3.connect('db/database.db')
    users.remove_user(conn, user_id)

# WORDLIST
def get_random_words(num: int):
    conn = sqlite3.connect('db/database.db')
    
    res = words.get_random_words(conn, num) 

    return res

def add_word_to_wordlist(user_id: int, word: str):
    conn = sqlite3.connect('db/database.db')
    is_learned = user_learned_words.get_user_learned_word(conn, user_id, word)
    if(is_learned):
        user_learned_words.remove_user_learned_word(conn, user_id, word)

    # add user and word if don't exist
    users.add_user(conn, user_id)
    words.add_word(conn, word, 'it')

    user_words.add_user_word(conn, user_id, word)

def remove_word_from_wordlist(user_id: int, word: str):
    conn = sqlite3.connect('db/database.db')
    user_words.remove_user_word(conn, user_id, word)
    user_learned_words.remove_user_learned_word(conn, user_id, word)

def word_learned(user_id: int, word: str):
    conn = sqlite3.connect('db/database.db')
    user_learned_words.add_user_learned_word(conn, user_id, word)

    user_words.remove_user_word(conn, user_id, word)