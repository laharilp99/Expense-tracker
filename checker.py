from maindb import get_connection

def list_tables():
    conn = get_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print("-", table[0])
    else:
        print("No tables found in the database.")

if __name__ == '_main_':
    list_tables()