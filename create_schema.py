import sqlite3

conn = sqlite3.connect('instance/expense.db')
cursor = conn.cursor()

cursor.execute("ALTER TABLE expensetrack ADD COLUMN username TEXT")
conn.commit()
conn.close()