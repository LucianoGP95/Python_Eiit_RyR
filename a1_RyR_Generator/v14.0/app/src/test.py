import os
import sqlite3

filepath = os.path.dirname(__file__)
print(os.path.abspath("../5_database"))

conn = sqlite3.connect((os.path.join(filepath, "test.db")))