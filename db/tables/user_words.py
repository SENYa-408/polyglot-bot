from sqlite3 import Connection

def add_user_word(conn: Connection, user_id: int, word: str):
    cur = conn.cursor()
    cur.execute('''
                INSERT OR IGNORE INTO user_words (user_id, word) VALUES (?, ?)
                ''', (user_id, word))
    conn.commit()
    cur.close()

def get_all_user_words(conn: Connection, user_id: int):
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM user_words WHERE user_id = ?
                ''', (user_id,))
    res = cur.fetchall()
    conn.commit()
    cur.close()

    return res

def get_user_word(conn: Connection, user_id: int, word: str):
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM user_words WHERE user_id = ? AND word = ?
                ''', (user_id, word))
    res = cur.fetchall()
    conn.commit()
    cur.close()

    return res

def remove_user_word(conn: Connection, user_id: int, word: str):
    cur = conn.cursor()
    cur.execute('''
                DELETE FROM user_words WHERE user_id = ? AND word = ?
                ''', (user_id, word))
    conn.commit()
    cur.close()
