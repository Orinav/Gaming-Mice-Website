import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'mice_catalog.db')


def get_mice_database():
    mice_database = sqlite3.connect(DB_PATH)
    mice_database.row_factory = sqlite3.Row
    return mice_database


def initialize_mice_database():
    mice_database = get_mice_database()
    cursor = mice_database.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS mice
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       brand
                       TEXT
                       NOT
                       NULL,
                       model
                       TEXT
                       NOT
                       NULL,
                       weight_grams
                       INTEGER,
                       sensor
                       TEXT
                       NOT
                       NULL,
                       image_url
                       TEXT,
                       buy_url
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       password
                       TEXT
                       NOT
                       NULL
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS favorites
                   (
                       user_id
                       INTEGER,
                       mouse_id
                       INTEGER,
                       PRIMARY
                       KEY
                   (
                       user_id,
                       mouse_id
                   ),
                       FOREIGN KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       mouse_id
                   ) REFERENCES mice
                   (
                       id
                   )
                       )
                   ''')

    cursor.execute('SELECT COUNT(*) AS total_users FROM users')
    if cursor.fetchone()['total_users'] == 0:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', '1234'))
        print("👤 Default user created (ID: 1)")

    mice_database.commit()
    mice_database.close()
    print("✅ Database tables initialized successfully.")


def insert_scraped_mice(mice_list):
    db = get_mice_database()
    cursor = db.cursor()

    for mouse in mice_list:
        cursor.execute('SELECT id FROM mice WHERE brand = ? AND model = ?', (mouse['brand'], mouse['model']))
        if not cursor.fetchone():
            cursor.execute('''
                           INSERT INTO mice (brand, model, weight_grams, sensor, image_url, buy_url)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', (mouse['brand'], mouse['model'], mouse['weight'], mouse['sensor'], mouse['image'],
                                 mouse['url']))
    db.commit()
    db.close()
    print(f"🖱️ Inserted {len(mice_list)} new scraped mice into database.")


def add_mouse_to_mice_database(brand, model, weight, sensor, image, buy_url):
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('''
                   INSERT INTO mice (brand, model, weight_grams, sensor, image_url, buy_url)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''', (brand, model, weight, sensor, image, buy_url))
    db.commit()
    db.close()


def delete_mouse_from_mice_database(mouse_id):
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('DELETE FROM mice WHERE id = ?', (mouse_id,))
    db.commit()
    db.close()


def add_to_favorites(user_id, mouse_id):
    db = get_mice_database()
    cursor = db.cursor()
    try:
        cursor.execute('INSERT INTO favorites (user_id, mouse_id) VALUES (?, ?)', (user_id, mouse_id))
        db.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        db.close()


def remove_from_favorites(user_id, mouse_id):
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('DELETE FROM favorites WHERE user_id = ? AND mouse_id = ?', (user_id, mouse_id))
    db.commit()
    db.close()


def get_user_favorites(user_id):
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('''
                   SELECT mice.*
                   FROM mice
                            JOIN favorites ON mice.id = favorites.mouse_id
                   WHERE favorites.user_id = ?
                   ''', (user_id,))
    favs = [dict(row) for row in cursor.fetchall()]
    db.close()
    return favs