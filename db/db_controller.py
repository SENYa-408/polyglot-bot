import sqlite3
from db.tables import create_tables, users, words, user_words, user_learned_words 

DB_PATH = 'db/database.db'

def init():
    conn = sqlite3.connect(DB_PATH)
    create_tables.init_tables(conn)

# USERS
def add_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    users.add_user(conn, user_id)

def get_dict_code(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    user = users.get_user(conn, user_id)

    return user[0][1]

def update_user_dict(user_id: int, value: str):
    conn = sqlite3.connect(DB_PATH)
    users.update_user(conn, user_id, value, 'dictionary')

def remove_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    users.remove_user(conn, user_id)

# WORDLIST
def get_all_learned_words(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    
    learned_words = user_learned_words.get_all_user_learned_words(conn, user_id)
    res = []
    for el in learned_words:
        res.append(el[1])
    
    return res
    

def get_all_words(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    
    words = user_words.get_all_user_words(conn, user_id)
    res = []
    for el in words:
        res.append(el[1])
    
    return res


def get_random_words(num: int):
    conn = sqlite3.connect(DB_PATH)
    
    res = words.get_random_words(conn, num) 

    return res

def add_word_to_wordlist(user_id: int, word: str):
    conn = sqlite3.connect(DB_PATH)
    is_learned = user_learned_words.get_user_learned_word(conn, user_id, word)
    if(is_learned):
        user_learned_words.remove_user_learned_word(conn, user_id, word)

    user = users.get_user(conn, user_id)

    # add user and word if don't exist
    users.add_user(conn, user_id)
    words.add_word(conn, word, user[0][1])

    user_words.add_user_word(conn, user_id, word)

def remove_word_from_wordlist(user_id: int, word: str):
    conn = sqlite3.connect(DB_PATH)
    user_words.remove_user_word(conn, user_id, word)
    user_learned_words.remove_user_learned_word(conn, user_id, word)

def word_learned(user_id: int, word: str):
    conn = sqlite3.connect(DB_PATH)
    user_learned_words.add_user_learned_word(conn, user_id, word)

    user_words.remove_user_word(conn, user_id, word)