import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'mice_catalog.db')


def db_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def db_init():
    try:
        with db_connection() as connection: #First with = closing the file.
            with connection: #Second with = commiting the file.
                cursor = connection.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mice
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        brand TEXT,
                        model TEXT,
                        weight_grams REAL,
                        sensor TEXT,
                        length REAL,
                        width REAL,
                        height REAL,
                        shape_top TEXT,
                        shape_side TEXT,
                        image_url TEXT
                    )
                ''')
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.exception(f'Error in initializing the database: {e}')

def db_insert(mice):
    query = '''
        INSERT INTO mice (brand, model, weight_grams, sensor, length, width, height, shape_top, shape_side, image_url)
        VALUES (:brand, :model, :weight_grams, :sensor, :length, :width, :height, :shape_top, :shape_side, :image_url)
    '''
    try:
        with db_connection() as connection:
            with connection:
                cursor = connection.cursor()
                for mouse in mice:
                    cursor.execute(query, mouse)
        mice_amount = len(mice)
        logger.info(f'Inserted {mice_amount} mice into the database.')
    except Exception as e:
        logger.exception(f'Error inserting mice into database: {e}')

def db_delete(mouse_id):
    try:
        with db_connection() as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM mice WHERE id = ?", (mouse_id,))
    except Exception as e:
        logger.exception(f'Error deleting mice from database: {e}')

def db_reset():
    try:
        with db_connection() as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute("DROP TABLE IF EXISTS mice")
        logger.info("Mice table dropped.")
        db_init()
    except Exception as e:
        logger.exception(f'Error resetting mice table: {e}')

def db_get_mice():
    try:
        with db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM mice")
            rows = cursor.fetchall()
        mice_list = []
        for row in rows:
            mice_list.append(dict(row))
        return mice_list
    except Exception as e:
        logger.exception(f'Error getting mice list: {e}')
        return []