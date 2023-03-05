from sqlite3 import Connection

def init_tables(conn: Connection):
    cur = conn.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    quizzes_answered INTEGER,
                    quizzes_answered_correct INTEGER
                )
                ''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    word VARCHAR(255) PRIMARY KEY,
                    language VARCHAR(255) NOT NULL
                )
                ''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS user_words (
                    user_id INTEGER NOT NULL,
                    word VARCHAR(255) NOT NULL,
                    PRIMARY KEY (user_id, word),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (word) REFERENCES words(word)
                )
                ''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS user_learned_words (
                    user_id INTEGER NOT NULL,
                    word VARCHAR(255) NOT NULL,
                    PRIMARY KEY (user_id, word),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (word) REFERENCES words(word)
                )
                ''')

    conn.commit()
    cur.close()
    conn.close()