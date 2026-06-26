import sqlite3
conn = sqlite3.connect("bluestock_mf.db")
print("Database created successfully")
conn.close()