import sqlite3

conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()

with open("sql/schema.sql", "r") as f:
    sql_script = f.read()

statements = sql_script.split(";")

for i, statement in enumerate(statements):
    statement = statement.strip()
    if statement:
        try:
            cursor.execute(statement)
            print(f"Statement {i+1} executed successfully")
        except Exception as e:
            print(f"Error in statement {i+1}:")
            print(statement)
            print(e)
            break


conn.commit()
conn.close()