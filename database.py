import sqlite3

class Database:
    def __init__(self, db_name='LastHope2.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_database()

    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                                chat_id INTEGER PRIMARY KEY,
                                answer TEXT,
                                city TEXT,
                                tokens INTEGER,
                                history TEXT,
                                score INTEGER,
                                country TEXt
                            )''')


    def add_user(self, chat_id, tokens = 4000, answer=None, city=None, history=None, score=0, country="Россия"):
        self.cursor.execute("INSERT OR IGNORE INTO tokens (chat_id, tokens, answer, city, history, score, country) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (chat_id, tokens, answer, city, history, score, country))
        self.conn.commit()

    def count_users(self, chat_id):
        try:
            self.cursor.execute('''SELECT COUNT(DISTINCT chat_id) FROM tokens WHERE chat_id <> ?''', (chat_id,))
            count = self.cursor.fetchone()[0]
            return count
        except Exception as e:
            print(e)
            return None

    ###-------------------------------------------------------------------------------------------------------------------------###
    ###-------------------------------------------------------------------------------------------------------------------------###

    def get_country(self, chat_id):
        self.cursor.execute("SELECT country FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def get_score(self, chat_id):
        self.cursor.execute("SELECT score FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_tokens(self, chat_id):
        self.cursor.execute("SELECT tokens FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_city(self, chat_id):
        self.cursor.execute("SELECT city FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_answer(self, chat_id):
        self.cursor.execute("SELECT answer FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None



    ###-------------------------------------------------------------------------------------------------------------------------###
    ###-------------------------------------------------------------------------------------------------------------------------###

    def update_answer(self, answer, chat_id):
        self.cursor.execute(
            f"UPDATE tokens SET answer = '{answer}' WHERE chat_id = ?", (chat_id,))
        self.conn.commit()

    def update_country(self, country, chat_id):
        self.cursor.execute(
            f"UPDATE tokens SET country = '{country}' WHERE chat_id = ?", (chat_id,))
        self.conn.commit()

    def update_score(self, score, chat_id):
        self.cursor.execute(
            f"UPDATE tokens SET score = '{score}' WHERE chat_id = ?", (chat_id,))
        self.conn.commit()

    def update_city(self, city, chat_id):
        self.cursor.execute(
            f"UPDATE tokens SET city = '{city}' WHERE chat_id = ?", (chat_id,))
        self.conn.commit()


    def update_history(self, history, chat_id):
        self.cursor.execute(
            f"UPDATE tokens SET history = '{history}' WHERE chat_id = ?", (chat_id,))
        self.conn.commit()


    def update_tokens(self, user_tokens, chat_id):
        self.cursor.execute("SELECT tokens FROM tokens WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()

        tokens = result[0]
        total_tokens = tokens - user_tokens

        self.cursor.execute(
            f"UPDATE tokens SET tokens = '{total_tokens}' WHERE chat_id = ?", (chat_id,))
        self.conn.commit()


    def close(self):
        self.conn.close()