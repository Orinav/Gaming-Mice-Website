import sqlite3

def get_mice_database():
    mice_database = sqlite3.connect('mice_catalog.db')
    mice_database.row_factory = sqlite3.Row
    return mice_database

def initialize_mice_database():
    mice_database = get_mice_database()
    cursor = mice_database.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS mice
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       brand TEXT NOT NULL,
                       model TEXT NOT NULL,
                       weight_grams INTEGER,
                       grip_style TEXT,
                       sensor TEXT NOT NULL,
                       image_url TEXT,
                       buy_url TEXT
                   )
                   ''')
                       
    mice_database.commit()
    mice_database.close()

def insert_sample_mice():
    mice_database = get_mice_database()
    cursor = mice_database.cursor()

    cursor.execute('SELECT COUNT(*) AS total_mice FROM mice')
    row = cursor.fetchone()

    if row['total_mice'] == 0:
        sample_data = [
            ('Logitech', 'G PRO X Superlight 2', 60, 'Claw/Fingertip/Palm', 'HERO 2', '/images/superlight2.jfif', 'https://www.logitechg.com/en-eu/shop/p/pro-x2-superlight-wireless-mouse'),
            ('Logitech', 'G Pro X2 Superstrike', 60, 'Claw/Fingertip/Palm', 'HERO 2', '/images/superstrike.jpg','https://www.logitechg.com/en-eu/shop/p/pro-x2-superstrike-mouse.910-007777'),
            ('Razer', 'Viper V3 Pro', 55, 'Claw/Fingertip/Palm', 'Focus Pro 35K Gen-2', '/images/viper_v3_pro.jpg','https://www.razer.com/gaming-mice/razer-viper-v3-pro'),
            ('Ninjutso', 'Sora V2', 39, 'Claw/Fingertip', 'PixArt PAW3395', '/images/sora_v2.JPG','https://ninjutso.com/products/ninjutso-sora-v2')
        ]

        for mouse in sample_data:
            cursor.execute('''
                           INSERT INTO mice (brand, model, weight_grams, grip_style, sensor, image_url, buy_url)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           ''', mouse)
            mice_database.commit()

    mice_database.close()

def add_mouse_to_mice_database(brand, model, weight, grip, sensor, image, buy_url):
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO mice (brand, model, weight_grams, grip_style, sensor, image_url, buy_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (brand, model, weight, grip, sensor, image, buy_url))
    db.commit()
    db.close()

def delete_mouse_from_mice_database(mouse_id):
    db = get_mice_database()
    cursor = db.cursor()
    cursor.execute('DELETE FROM mice WHERE id = ?', (mouse_id,))
    db.commit()
    db.close()