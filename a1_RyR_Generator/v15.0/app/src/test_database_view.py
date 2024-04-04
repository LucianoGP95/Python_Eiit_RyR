import tkinter as tk
from tkinter import ttk
import sqlite3

def populate_treeview():
    # Connect to SQLite database
    conn = sqlite3.connect(r"C:\Codebase\Python_Eiit_RyR\a1_RyR_Generator\v15.0\5_database\RyR_data.db")
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute('SELECT * FROM your_table')
    data = cursor.fetchall()

    # Populate the treeview with data
    for row in data:
        treeview.insert('', 'end', values=row)

    # Close database connection
    conn.close()

# Create the main window
main_window = tk.Tk()
main_window.title('Database Visualization App')

# Create a treeview to display database records
treeview = ttk.Treeview(main_window, columns=('Column 1', 'Column 2'))
treeview.heading('#0', text='ID')
treeview.heading('Column 1', text='Column 1')
treeview.heading('Column 2', text='Column 2')
treeview.pack()

# Populate the treeview with data when the app starts
populate_treeview()

# Start the Tkinter event loop
main_window.mainloop()
