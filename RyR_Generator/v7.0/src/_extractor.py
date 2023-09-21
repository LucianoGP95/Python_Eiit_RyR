import sys
sys.path.append("../tools/")
import _db_tools

def database():
    dbh = _db_tools.SQLite_Data_Extractor("database.db") 
    dbh.store_directory("../../1_Place_Reports_Here/")
    dbh.consult_tables()

#test script
if __name__ == "__main__":
    database()