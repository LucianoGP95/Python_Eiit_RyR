import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import core_logic

### Robust paths creation
src_dir = os.path.dirname(os.path.realpath(sys.executable) if getattr(sys, 'frozen', False) else __file__)
root_path = os.path.dirname(src_dir)
input_path = os.path.join(root_path, "a1_input")
output_path = os.path.join(root_path, "a2_output")
filepath = os.path.join(root_path, os.path.join("folder", "file"))

### Globals
filepath = ""

### Callback functions
def ask_filepath(directory_entry):
    '''Opens a dialog window to select the source file and auto updates the rows'''
    global filepath, df
    file_path = filedialog.askopenfilename()  #Use askopenfilename to get the file path
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, file_path)
    filepath = file_path
    df = core_logic.import_file(filepath)  #Pass the file path to your import_file function
    return filepath, df

def plot(df, filter_entry):
    '''Plot dataframes'''
    try:
        filter_value = filter_entry.get()
        core_logic.plot(df, filter_value)
    except Exception as e:
        messagebox.showerror("Error", e)

def placeholder_callback():
    """Widget command"""
    ...

def on_right_click(event):
    """Event binding"""
    context_menu.post(event.x_root, event.y_root)

def top_menu_tab():
    """Creation of tab for top bar menu"""
    messagebox.showinfo("sub-menu", "Text")

### Window object creation
root = tk.Tk()
root.title("Tkinter Template")
root.geometry()
frame = ttk.Frame(root, width=800, height=600)
frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

### Top bar menu creation
menu = tk.Menu(root)
root.config(menu=menu)
about_menu = tk.Menu(menu)
menu.add_cascade(label="sub-menu", menu=about_menu)
about_menu.add_command(label="tab", command=top_menu_tab)

### Widgets creation
directory_entry = ttk.Entry(frame, width=150)
filter_entry = ttk.Entry(frame)
import_button = ttk.Button(frame, text="Import", command=lambda: ask_filepath(directory_entry))
database_button = ttk.Button(frame, text="Database", command=placeholder_callback)
plot_button = ttk.Button(frame, text="Plot", command=lambda: plot(df, filter_entry))

### Widgets placement
import_button.grid(row=1, column=0, pady=10)
directory_entry.grid(row=2, column=0, pady=10)
database_button.grid(row=3, column=0, pady=10)
filter_entry.grid(row=4, column=0, pady=10)
plot_button.grid(row=5, column=0, pady=10)

### Context menu
context_menu = tk.Menu(root, tearoff=0)

### Main event loop
root.mainloop()
