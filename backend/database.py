import sqlite3

def get_mice_database():
    # Create new database file named 'mice_catalog.db'.
    mice_database = sqlite3.connect('mice_catalog.db')
    # Making possible to address the database file by its columns names.
    mice_database.row_factory = sqlite3.Row
    return mice_database


def initialize_mice_database():
    # Connect to our database (the file we created earlier).
    mice_database = get_mice_database()
    # Creating a cursor, cursor is an object that runs all the SQL commands.
    cursor = mice_database.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS mice
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       brand TEXT NOT NULL,
                       model TEXT NOT NULL,
                       weight_grams INTEGER,
                       grip_style TEXT,
                       sensor TEXT NOT NULL
                   )
                   ''')

    # Save changes
    mice_database.commit()
    # Close file to release computer resources and to deprive the file being locked
    mice_database.close()


def insert_sample_mice():
    mice_database = get_mice_database()
    cursor = mice_database.cursor()


    cursor.execute('SELECT COUNT(*) AS total_mice FROM mice')
    # Take the next row(only the first row this time) from the last query
    row = cursor.fetchone()

    if row['total_mice'] == 0:
        sample_data = [
            ('Logitech', 'G PRO X Superlight 2', 60, 'Claw/Fingertip/Palm', 'HERO 2'),
            ('Logitech', 'G Pro X2 Superstrike', 60, 'Claw/Fingertip/Palm', 'HERO 2'),
            ('Razer', 'Viper V3 Pro', 55, 'Claw/Fingertip/Palm', 'Focus Pro 35K Gen-2'),
            ('Ninjutso', 'Sora V2', 39, 'Claw/Fingertip', 'PixArt PAW3395')
        ]

        for mouse in sample_data:
            cursor.execute('''
                           INSERT INTO mice (brand, model, weight_grams, grip_style, sensor)
                           VALUES (?, ?, ?, ?, ?)
                           ''', mouse)
            mice_database.commit()

    mice_database.close()