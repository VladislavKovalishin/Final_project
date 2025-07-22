import sqlite3

conn = sqlite3.connect('bot_db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bot_db(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date_user DATE NOT NULL,
    time_user TIME NOT NULL,
    user_text TEXT NOT NULL
    )
''')

conn.commit()


def add_entry(user_id, date_user, time_user, user_text):
    cursor.execute('''
        INSERT INTO bot_db (user_id, date_user, time_user, user_text)
        VALUES (?, ?, ?, ?)
    ''', (user_id, date_user, time_user, user_text))
    conn.commit()


def search_entry(user_id):
    cursor.execute('''
        SELECT * FROM bot_db WHERE user_id=?
    ''', (user_id,))
    return cursor.fetchall()


def delete_entry(id_entry):
    cursor.execute('''
    DELETE FROM bot_db WHERE id=?
    ''', (id_entry,))
    conn.commit()


def get_date_time_entry(user_id):
    cursor.execute('''
    SELECT id, date_user, time_user FROM bot_db WHERE user_id=?
    ''', (user_id,))


def get_reminder_id(user_id):
    cursor.execute('''
    SELECT id FROM bot_db WHERE user_id=?
    ''', (user_id,))
    return cursor.fetchall()
