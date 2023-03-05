from sqlite3 import Connection, IntegrityError

def add_word(conn: Connection, word: str, language: str):
    cur = conn.cursor()
    try:
        cur.execute('''
                    INSERT OR IGNORE INTO words (word, language) VALUES (?, ?)
                    ''', (word, language))
        conn.commit()
    except IntegrityError:
        return False

    cur.close()
    return True

def get_word(conn: Connection, word: str):
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM words WHERE word = ?
                ''', (word,))
    res = cur.fetchall()
    conn.commit()
    cur.close()

    return res

def get_random_words(conn: Connection, num: int):
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM words ORDER BY RANDOM() LIMIT ?
                ''', (num,))
    res = cur.fetchall()
    conn.commit()
    cur.close()

    return res

def remove_word(conn: Connection, word: str):
    cur = conn.cursor()
    cur.execute('''
                DELETE FROM words WHERE word = ?
                ''', (word,))
    conn.commit()
    cur.close()