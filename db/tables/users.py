from sqlite3 import Connection

def add_user(conn: Connection, user_id: int):
    cur = conn.cursor()
    cur.execute('''
                INSERT OR IGNORE INTO users (user_id) VALUES (?)
                ''', (user_id,))
    conn.commit()
    cur.close()

def get_user(conn: Connection, user_id: int):
    cur = conn.cursor()
    cur.execute('''
                SELECT * FROM users WHERE user_id = ?
                ''', (user_id,))
    res = cur.fetchall()
    conn.commit()
    cur.close()

    return res

def remove_user(conn: Connection, user_id: int):
    cur = conn.cursor()
    cur.execute('''
                DELETE FROM users WHERE user_id = ?
                ''', (user_id,))
    conn.commit()
    cur.close()