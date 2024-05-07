#Import packages, modules, functions and variables
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
...
sys.path.append("./placeholder_path") #location of custom modules
... #import custom modules

#Robust paths creation
src_dir = os.path.dirname(os.path.realpath(sys.executable) if getattr(sys, 'frozen', False) else __file__)
root_path = os.path.dirname(src_dir)
folderpath = os.path.join(root_path, "folder")
filepath = os.path.join(root_path, os.path.join("folder", "file"))
...

### Callback functions
def on_button_click():
    """Widget command"""
    entry_text = entry.get()
    label_output.config(text=f"Hello, {entry_text}!")

def on_right_click(event):
    """Event binding"""
    context_menu.post(event.x_root, event.y_root)

def on_context_menu_selection():
    """Context menu creation"""
    label_output.config(text="Right-click menu selected!")

def top_menu_tab():
    """creation of tab for top bar menu"""
    messagebox.showinfo("sub-menu", "Text")

### Window object creation
root = tk.Tk()
root.title("Tkinter Template")
root.geometry("400x200")

### Top bar menu creation
menu = tk.Menu(root)
root.config(menu=menu)
about_menu = tk.Menu(menu)
menu.add_cascade(label="sub-menu", menu=about_menu)
about_menu.add_command(label="tab", command=top_menu_tab)

### Widgets creation
label = ttk.Label(root, text="Enter your name:")
label.pack(pady=10)

entry = ttk.Entry(root)
entry.pack(pady=5)

button = ttk.Button(root, text="Click Me!", command=on_button_click)
button.pack(pady=10)

label_output = ttk.Label(root, text="")
label_output.pack(pady=5)

### Context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Menu Option", command=on_context_menu_selection)

### Keys Bindding
label.bind("<Button-3>", on_right_click)

### Main event loop
root.mainloop()
