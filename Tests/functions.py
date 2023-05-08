import tkinter as tk
import tkinter.filedialog

def askdirectory(text_field):
    source_dirname = tk.filedialog.askdirectory()
    text_field.delete(0, tk.END)
    text_field.insert(0, source_dirname)
    return source_dirname

def asktarget(text_field):
    target_dirname = tk.filedialog.askopenfilename()
    text_field.delete(0, tk.END)
    text_field.insert(0, target_dirname)
    return target_dirname

""" if selected_option == options[0]:
    print("2")
else:
    print("4") """