import pandas as pd
import sqlite3
import os

S = 50
conn = sqlite3.connect("../database/lookup_table.db")

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"The tables inside the database are:")
for table in tables:
    print(table[0])

cursor = conn.cursor()
cursor.execute(f"SELECT * FROM awg;")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor = conn.cursor()
cursor.execute(f"SELECT * FROM awg WHERE section >= {S};")
result = cursor.fetchall()
print(f"The specific section value is:")
for row in result:
    print(row)  # Index 0 corresponds to the first column




