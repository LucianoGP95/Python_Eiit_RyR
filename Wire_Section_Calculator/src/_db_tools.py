import pandas as pd
import sqlite3

class dbHandler:
    def __init__(self, source_name, db_name):
        self.excel_path = "../references/" + source_name
        self.db_path = "../database/" + db_name
        self.df = None
        self.conn = None
        self.table_name = None
    def connect_from_excel(self):
        try:
            self.df = pd.read_excel(self.excel_path)
            self.conn = sqlite3.connect(self.db_path)  # Will create the db if it doesn't exist
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")
    def create_table(self, table_name):
        try:
            if not self.conn:
                raise Exception("Database connection is not established.")
            # Validate the table_name here, e.g., check for valid characters
            if not table_name.isalnum():
                raise Exception("Invalid table name.")
            self.table_name = table_name
            self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            print(f'Data from {self.excel_path} has been imported into the *{self.table_name}* table in {self.db_path}.')
        except Exception as e:
            raise Exception(f"Error creating table in database: {str(e)}")
    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error making a commit in {self.table_name}: {str(e)}")
    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            raise Exception(f"Error closing database connection: {str(e)}")
    def create_cursor(self):
        try:
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as e:
            raise Exception(f"Error creating a cursor: {str(e)}")
    def execute_query(self, query):
        try:
            if not self.cursor:
                raise Exception("Cursor is not created.")
            self.cursor.execute(query)
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

#Test script
if __name__ == '__main__':
    dbh = dbHandler("awg_sections.xlsx", "lookup_table.db")
    dbh.connect()
    print(dbh.conn.tables)
    dbh.close()