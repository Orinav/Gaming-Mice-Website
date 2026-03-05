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

    # השארנו אך ורק את טבלת העכברים!
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS mice
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       brand TEXT NOT NULL,
                       model TEXT NOT NULL,
                       weight_grams INTEGER,
                       sensor TEXT NOT NULL,
                       image_url TEXT,
                       buy_url TEXT
                   )
                   ''')

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