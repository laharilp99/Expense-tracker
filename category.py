from maindb import get_connection


def create_category_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category (
            slno INTEGER PRIMARY KEY AUTOINCREMENT,
            catname TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()