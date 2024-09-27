import mysql.connector
import sqlite3

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="toor",
    database="your_mysql_database"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM your_table")
data = cursor.fetchall()
cursor.close()

print(data)