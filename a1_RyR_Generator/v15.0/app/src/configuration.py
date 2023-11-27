import os, json, sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def add_format(format_check):
    # This function will be called when the checkbox is clicked
    if format_check.get():
        messagebox.showinfo("Attention!", "Format added to the output!\n\nDatabase data remains equal.")

def close_window(conf):
    conf.withdraw() #Hides the window again after
    conf.grab_release() #Unfreezes the root window   