#V12.0 13/11/2023
import os, json, time
import pandas as pd
import sqlite3
from urllib.parse import urlparse
import shutil
#Secondary requirements: pip install openpyxl
################################################################################
class SQLite_Handler:
    '''SQLite custom handler'''
    def __init__(self, db_name: str, rel_path=None):
        if rel_path == None:
            self.db_path: str = os.path.join(os.path.abspath("../database/"), db_name)
        else: #Optional relative path definition
            try:
                self.db_path: str = os.path.join(os.path.abspath(rel_path), db_name)
            except OSError as e:
                print(f"Error with custom path creation: {e}")
        self.df: pd.DataFrame = None
        self.conn = None
        self.cursor = None
        self.conn = sqlite3.connect(self.db_path) #Preventive connection/creation to the database
        self.cursor = self.conn.cursor()
        if not os.path.exists(self.db_path): 
            print(f"Database *{db_name}* created in: {self.db_path}")
        else: 
            print(f"Database *{db_name}* found in: {self.db_path}")

    def rename_table(self, old_name: str, new_name: str):
        try:
            self.cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name};")
            self.conn.commit()
            print(f"Table *{old_name}* renamed to *{new_name}*")
        except Exception as e:
            raise Exception(f"Error while renaming table: {str(e)}")

    def delete_table(self, table_name: str):
        try:
            print(f"Warning: This action will drop the table {table_name}.")
            confirmation = input("Do you want to continue? (y/n): ").strip().lower()
            if confirmation == 'y':
                self.cursor.execute(f"DROP TABLE {table_name};")
                self.conn.commit()
                print(f"{table_name} dropped successfully.")
                print(f"Table *{table_name}* deleted")
                self.consult_tables()
            else:
                print("Operation canceled.")
        except Exception as e:
            raise Exception(f"Error while deleting table: {str(e)}")

    def delete_row(self, row_name: str, table_name: str):
        '''Drops row(s) from the desired table'''
        row_name = self._input_handler(row_name)
        try:
            print(f"Warning: This action will drop row(s) from {table_name}.")
            confirmation = input("Do you want to continue? (y/n): ").strip().lower()
            if confirmation == 'y':
                for row in row_name:
                    self.cursor.execute(f"PRAGMA table_info({table_name})")
                    columns_info = self.cursor.fetchall()
                    column_name= columns_info[0][1]
                    self.cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = '{row}'")
                    self.conn.commit()
                    print(f"{row} dropped successfully.")
                print(f"Row(s) deleted from table *{table_name}*")
                self.examine_table(table_name)
            else:
                print("Operation canceled.")
        except Exception as e:
            raise Exception(f"Error while deleting table: {str(e)}")

    def consult_tables(self):
        '''Shows all the tables in the database'''
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        _, file = os.path.split(self.db_path)
        print(f"{file} actual contents:")
        for table in tables:
            print(f"    {table[0]}")

    def examine_table(self, table_name: str):
        '''Prints the desired table or tables if given in list or tuple format'''
        table_name = self._input_handler(table_name)
        try:
            cursor = self.conn.cursor()
            for i, table in enumerate(table_name):
                print(f"table {i+1}: {table}")
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                rows = cursor.fetchone()[0]
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                columns_number = len(columns)
                column_names = []; rows = [] #Preallocation
                for column in columns: #Get column names
                    column_name = column[1]
                    column_names.append(column_name)
                column_names = tuple(column_names)
                print(f"    Rows: {rows}\n    Columns: {columns_number}")
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()
                print(f"Columns name: {column_names}")
                for row in rows: #Gets values row by row
                    print(f"    {row}")
        except Exception as e:
            raise Exception(f"Error while examining tables: {(e)}")

    def close_conn(self):
        '''Closes the database connection when done'''
        try:
            self.conn.close()  
            print(f"Closed connection to: {self.db_path}")
        except Exception as e:
            print(f"Error clearing the database: {str(e)}")

    def reconnect(self, *argv):
        '''Connects to the either the same database or other database. *argv[0] holds the new database name'''
        if argv and len(argv) > 0 and argv[0] is not None: #Checks if the new database was passed as an argument
            self.db_path = os.path.join(os.path.abspath("../database"), argv[0])            
        try: #Ensures the db was closed
            self.conn.close() 
        except Exception:
            pass
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"Connected to {self.db_path}")

    def clear_database(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #Get a list of all tables in the database
            tables = cursor.fetchall()
            _, file = os.path.split(self.db_path)
            confirmation = input(f"Warning: This action will clear all data from the database {file}.\nDo you want to continue? (y/n): ").strip().lower()
            if confirmation == 'y':
                for table in tables: #Loop through the tables and delete them
                    table_name = table[0]
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                self.conn.commit()
                print("Database cleared successfully.")
            else:
                print("Operation canceled.")
        except Exception as e:
            print(f"Error clearing the database: {str(e)}")
    '''internal methods'''
    def _input_handler(self, input):
        '''Modfifies the input parameter to handle several types and always return and iterable'''
        if isinstance(input, str):
            input = [input]
            return input
        elif isinstance(input, (list, tuple)):
            return input
        else:
            raise Exception(f"Unsupported input format: Try str, list, tuple.")
################################################################################
class SQLite_Data_Extractor(SQLite_Handler):
    '''Extracts structured data from different sources and turns it into a table in a database for quick deployment. Creates a db 
    from raw data or adds tables to it from raw data'''
    def __init__(self, db_name, rel_path):
        super().__init__(db_name, rel_path)  #Calls the parent class constructor
        self.source_name = None
        self.sep = ","

    def store(self, source):
        '''Generates table(s) of the given name using data from different sources'''
        self.source_name = source
        self._inputhandler() #Handles the source input format
        for i, source in enumerate(self.source_path):
            self._filetypehandler(source) #Handles the filetype
            if self.extension == "xlsx":
                self._datasheet_excel(i, source)
            if self.extension == "csv":
                self._datasheet_csv(i, source)
        try: #Incase there is a problem with the parent method
            self.consult_tables()
        except Exception as e:
            pass

    def store_directory(self, *argv):
        '''Generates table(s) for all the compatible files inside the custom directory. If the directory isn't given it uses 
        ../data/'''
        print(len(argv))
        if argv and len(argv) > 0:
            try:
                self.source_path = [argv[0] + name for name in os.listdir(argv[0])]
            except Exception as e:
                print("    Unrecognized directory. Using default one.")
        else:
            try: #Avoids errors if there isn't a "../data" path in the project
                self.source_path = ["../data/" + name for name in os.listdir("../data/")]
            except Exception as e:
                print("    No ../data/ directory, aborting operation")
        for i, source in enumerate(self.source_path):
            self._filetypehandler(source) #Handles the filetype
            if self.extension == "xlsx":
                self._datasheet_excel(i, source)
            if self.extension == "csv":
                self._datasheet_csv(i, source)
        try: #Incase there is a problem with the parent method
            self.consult_tables()
        except Exception as e:
            pass

    def store_df(self, df, table_name):
        '''Stores the desired dataframe as a table in the connected database.'''
        try:
            self.df = df
            self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
            self.conn.commit()
            print(f"Dataframe stored as *{table_name}*")
        except Exception as e:
            print(f"Error storing the dataframe: {str(e)}")

    def retrieve(self, table_name):
        '''Retrieves a table from the database as a dataframe object. If the arg. is a list or tuple it will try to concatenate
        all the tables'''
        if isinstance(table_name, str):
            try:
                self.cursor = self.conn.cursor()
                query = f"SELECT * FROM {table_name}"
                self.df = pd.read_sql(query, self.conn)
                print(f"Table *{table_name}* retrieved succesfully.")
                return self.df
            except Exception as e:
                print(f"Error retrieving table as dataframe: {str(e)}")
                return None
        if isinstance(table_name, (list, tuple)):
            dataframes = []
            for table in table_name:
                try:
                    self.cursor = self.conn.cursor()
                    query = f"SELECT * FROM {table}"
                    df = pd.read_sql(query, self.conn)
                    dataframes.append(df)
                    print(f"Table {table} retrieved succesfully.")
                except Exception as e:
                    print(f"Error retrieving table as dataframe: {str(e)}")
                    return None
            try:
                self.df = pd.concat(dataframes, ignore_index=True)
            except Exception as e:
                print(f"Error concatenating dataframes: {str(e)}")
        return self.df

    def set_csv_rules(self, sep=","):
        '''Used to modify the rules that pandas uses to parse csv files.'''
        try:
            self.sep = sep
        except Exception as e:
            print(f"Error changing the rules: {str(e)} \nCurrently supported: Separator")
        print(f"Updated rules:\nSeparator:{self.sep}")

    def rename_table(self, old_name, new_name):
        super().rename_table(old_name, new_name) 

    def delete_table(self, table_name):
        super().delete_table(table_name)  

    def consult_tables(self):
        super().consult_tables()

    def examine_table(self, table_name):
        super().examine_table(table_name) 

    def close_conn(self):
        super().close_conn()  

    def reconnect(self, *argv):
        super().reconnect(*argv) 

    def clear_database(self):
        super().clear_database() 

    '''Internal methods'''
    def _inputhandler(self):
        '''Handles variable quantity of elements. It accepts: 
            - A list or tuple indicating the desired files in ../data/
            - A string indicating a single file in ../data/
            - An url with a supported filetype'''
        self.flag = self._is_url(self.source_name) #Determines if the given source is an url
        if self.flag == True: 
            self.source_path = [self.source_name] #Converts the string to list to allow iteration with 1 element.
            print("url detected")
        else:
            if isinstance(self.source_name, str): 
                self.source_path = "../data/" + self.source_name
                self.source_path = [self.source_path] #Converts the string to list to allow iteration with 1 element.
            elif isinstance(self.source_name, (list, tuple)):
                self.source_path = ["../data/" + name for name in self.source_name]
            else:
                raise Exception(f"Error importing data: Data mas be specified in str, list or tuple format") 

    def _filetypehandler(self, source):
        '''Handles all the supported filetypes. Currently supported:
        - .csv
        - .xlsx (Excel)
        - Aun url pointing to a file of the above'''
        self.extension = source.split(".")[-1] #Gets the extension of the file
        match self.extension:
            case "xlsx":
                try:
                    self.df = pd.read_excel(source, sheet_name=None)
                except Exception as e:
                    raise Exception(f"Error importing data into pandas: {str(e)}")
            case "csv":
                try:
                    self.df = pd.read_csv(source, header=None, sep=self.sep)
                except Exception as e:
                    raise Exception(f"Error importing data into pandas: {str(e)}")
            case _:
                print(f"Unsupported file format: {source}, skipping file.")

    def _datasheet_excel(self, i, source):
        '''Specific method for sending .xlsx files with all their sheets as tables in the db'''
        try:
            print(f'Data from {source} has been imported to {self.db_path}.')
            print(f"Sheet(s) imported to db as table(s) with name(s):")
            for sheet_name, sheet in self.df.items():
                table_name = sheet_name
                if not sheet_name.isalnum(): #Ensures all tables always have legal characters (letters and numbers)
                    table_name = f"table{i+1}"
                    print(f"Invalid table name for sheet: {sheet_name}, adding it as table{i+1}")
                print(f"    {table_name}")
                sheet.to_sql(table_name, self.conn, if_exists='replace', index=False)
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

    def _datasheet_csv(self, i, source):
        '''Specific method for sending .csv files as tables in the db'''
        try:
            table_name = source.split(".")[-2].split("/")[-1]
            if not table_name.isalnum(): #Ensures all tables always have legal characters (letters and numbers)
                table_name = f"table{i+1}"
                print(f"Invalid table name: Adding it as table{i+1}")
            print(f'Data from {source} has been imported to {self.db_path}.')
            print(f"    {table_name}")
            self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        except Exception as e:
            raise Exception(f"Error connecting to database: {str(e)}")

    def _is_url(self, string):
        '''Determines whether the given argument is an url or not'''
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
################################################################################
class SQLite_Backup(SQLite_Handler):
    '''Automatic backup generator. Every time it runs it checks for an absolute 
    time condition comparing a .json file data with the specified backup time.'''
    def __init__(self, db_name, backup_folder=None, backup_time=None, rel_path=None):
        super().__init__(db_name, rel_path)  #Calls the parent class constructor
        if backup_folder is None: #Predefined path creation
            db_folder = os.path.abspath("../database/")
            self.backup_folder = os.path.join(db_folder, "backup")
        else: #Custom path creation
            self.backup_folder = os.path.realpath(backup_folder)
        print(f"Backup path: {self.backup_folder}")
        self.date, self.date_format = self._get_date(time.localtime())
        print(f"Current time: {self.date_format}")
        name_without_extension, _ = os.path.splitext(db_name)
        name = name_without_extension + ".json"
        self.json_path = os.path.join(self.backup_folder, name) #Default json name
        if backup_time is None: 
            self.backup_time = 10800 #Default backup time
        else:
            self.backup_time = backup_time
        self.check_backup(db_name)

    def create_checkpoint(self, db_name=None):
        '''Creates a first backup and a .json file to store the backup info.
        A specific db can be set for executing the method'''
        _, db_path = self._build_paths(db_name)
        _, name = os.path.split(db_path)
        name_without_extension, _ = os.path.splitext(name)
        database = name
        filename = name_without_extension + ".json"
        date = self.date
        data = { #json data creation
            "database": database,
            "filename": filename,
            "date": date,
            "date_format": self.date_format
            }
        self.json_path = os.path.join(self.backup_folder, filename)
        if os.path.exists(self.json_path): #Ensures no accidental overwritting
            confirmation = input(f"Warning: There is a checkpoint for that database\nDo you want to overwrite it? (y/n): ").strip().lower()
            if confirmation == 'y':
                with open(self.json_path, "w") as json_file:
                    json.dump(data, json_file) #Write the data to the JSON file
                print(f"Checkpoint *{filename}* created for *{database}* at *{self.date_format}*")
                self._backup(db_name=name)
        else:
            with open(self.json_path, "w") as json_file:
                json.dump(data, json_file) #Write the data to the JSON file
            print(f"Checkpoint *{filename}* created for *{database}* at *{self.date_format}*")
            self._backup(db_name=name)

    def manual_backup(self, db_name=None):
        '''Creates a manual backup by overwritting the json'''
        _, db_path = self._build_paths(db_name)
        _, name = os.path.split(db_path)
        with open(self.json_path, "r") as json_file:
            data = json.load(json_file)
            database = data["database"]
            filename = data["filename"]
        self.date, self.date_format = self._get_date(time.localtime())
        data = { #json data creation
            "database": database,
            "filename": filename,
            "date": self.date,
            "date_format": self.date_format
            }
        with open(self.json_path, "w") as json_file:
            json.dump(data, json_file) #Write the data to the JSON file
        print(f"Checkpoint *{filename}* created for *{database}* at *{self.date_format}*")
        self._backup(db_name=name)
    
    def check_backup(self, db_name):
        '''Quick auto-backup check'''
        if self.backup_time == -1:
            print("Backup disabled. Add a valid time amount to start it.")
            return
        print(f"Backup time period: {self._format_time(self.backup_time)} HH:MM:SS")
        self._auto_backup(db_name)

    def promote(self, db_name=None, backup_name=None):
        '''Restores the desired backup. Will destroy the specified database to replace.'''
        if db_name is None:
            raise ValueError("No main db defined")
        if backup_name is None:
            raise ValueError("No backup db defined")
        db_folder, db_path = self._build_paths(db_name=db_name)
        backup_path = os.path.join(self.backup_folder, backup_name)
        name = os.path.splitext(db_name)[0]
        backup = os.path.splitext(backup_name)[0]
        confirmation = input(f"Warning: This action will replace {name} for {backup}.\nDo you want to continue? (y/n): ").strip().lower()
        if confirmation == 'y':
            self.close_conn()
            shutil.copy(backup_path, db_path)
            print(f"Backup {backup} restored")
            self.reconnect()

    '''Internal methods'''
    def _auto_backup(self, db_name):
        '''Checks if the backup condition is met and returns related information'''
        current_time, current_date_format = self._get_date(time.localtime()) #Calculates the current time
        try:
            with open(self.json_path, "r") as json_file:
                data = json.load(json_file)
                json_date = data["date"] #Gets the checkpoit date
            left_to_backup = self.backup_time - (current_time - json_date) #Calculates the time left
            if left_to_backup >= self.backup_time:
                self._backup(db_name=db_name)
                print(f"Auto-Backup created at {current_date_format}")
            else:
                print(f"Time to next backup: {self._format_time(left_to_backup)}")
        except:
            print("Auto-backup failed. Check if a ckeckpoint for the db is created.")

    def _backup(self, db_name=None):
        '''Creates the backup'''
        _, current_date_format = self._get_date(time.localtime())
        db_name, _ = os.path.splitext(db_name)
        backup_name = f"{db_name}_backup_{current_date_format}.db"
        backup_path = os.path.join(self.backup_folder, backup_name)
        backup_db = sqlite3.connect(backup_path) #Creates the backup db
        self.conn.backup(backup_db)
        backup_db.close()
        print(f"*{backup_name}* has been created.")

    def _get_date(self, time_struct):
        '''Gets the current date in both numeric and readable time'''
        min = time_struct.tm_min; sec = time_struct.tm_sec
        day = time_struct.tm_mday; hour = time_struct.tm_hour
        year = time_struct.tm_year; month = time_struct.tm_mon
        current_date = sec + min*60 + hour*3600 + day*86400 + month*2592000 + year*946080000
        current_date_format = f"{year}y-{month:02d}m-{day:02d}d_{hour}h-{min:02d}m-{sec:02d}s"
        return current_date, current_date_format

    def _build_paths(self, db_name=None):
        '''Builds predefined or specific paths for the database'''
        if db_name is None: #Gets the predefined database
            db_folder, db_name = os.path.split(self.db_path)
            db_path = self.db_path
        else: #Gets specified database
            db_folder = os.path.dirname(self.db_path)
            db_path = os.path.join(db_folder, db_name)
        return db_folder, db_path

    def _format_time(self, seconds):
        '''Formats time in a HH:MM:SS fashion or converts "HH:MM:SS" string to seconds.'''
        if isinstance(seconds, (int, float)):
            hours, remainder = divmod(seconds, 3600)  # 3600 seconds in an hour
            minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
            formatted_time = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            return formatted_time
        elif isinstance(seconds, str):
            try:
                parts = seconds.split(':')
                hours, minutes, seconds = map(int, parts)
                total_seconds = hours * 3600 + minutes * 60 + seconds
                return total_seconds
            except Exception as e:
                raise Exception(f"Error while formatting the string: {e}")
        else:
            raise ValueError("Invalid input type. Use either int or 'HH:MM:SS' string for time input.")

###File Structure
#-Project root
#---Data (raw data)
#
#---Database (database location)
#------database.db
#------Backup
#---------checkpoint.json
#---------database_backup.db
#
#---Tools (script location)
#------_db_tools.py
#
###Test script
if __name__ == '__main__':
    #Creates or connects to a db in ../database/
    dbh = SQLite_Data_Extractor("database.db", rel_path=None)
    #Save a specific file inside ../data/
    dbh.store("data_2.xlsx")
    #Info of all tables
    dbh.consult_tables()
    #Show info and the contents of specific tables
    dbh.examine_table(["test1", "test2"])
    #Rename a table
    dbh.rename_table("test1", "new_test")
    #Get a table into a dataframe
    df = dbh.retrieve("new_test")
    #Close the connection when done
    dbh.close_conn()
    #Reconnect to the actual db or a new one
    dbh.reconnect()
    #Store the whole ../data/ directory or a custom one
    dbh.store_directory()
    
    #Create the backup manager
    bc = SQLite_Backup("database.db", backup_time=10800)
    #Create a checkpoint for the database to measure time since the last backup
    bc.create_checkpoint("database.db")
    #Generate a manual backup
    bc.manual_backup("database.db")
    #Check for the auto-backup
    bc.check_backup("database.db")
    #Restore a specific database backup. Requires both names input for safety.
    bc.promote("database.db", "database_backup_2023y-10m-20d_11h-58m-01s.db")
    
    ###WARNING zone###
    #Delete row(s)
    dbh.delete_row('a', "new_test")
    #Delete a single table
    dbh.delete_table("new_test")
    #Clear the database
    dbh.clear_database()