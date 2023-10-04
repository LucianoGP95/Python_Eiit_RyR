import os
import tkinter as tk
from tkinter import messagebox

def check_file_counts_2S(source_dirname):
    '''Checks if the number of files of each nest is even to avoid concatenating srrays of different size'''
    files = os.listdir(source_dirname)
    reports = [file for file in files if file.endswith(".csv")]
    i = sum(1 for filename1 in reports if "S1" in filename1)
    j = sum(1 for filename2 in reports if "S2" in filename2)
    if i != j:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Warning", "The number of files per nest is uneven, check they are the same number in the source folder and try again.")
        root.destroy()
        return

def check_file_counts_4S(source_dirname):
    '''Checks if the number of files of each nest is even to avoid concatenating srrays of different size'''
    files = os.listdir(source_dirname)
    reports = [file for file in files if file.endswith(".csv")]
    i = sum(1 for filename1 in reports if "S1" in filename1)
    j = sum(1 for filename2 in reports if "S2" in filename2)
    k = sum(1 for filename3 in reports if "S3" in filename3)
    l = sum(1 for filename4 in reports if "S4" in filename4)
    if i != j or i != k or i != l:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Warning", "The number of files per nest is uneven, check they are the same number in the source folder and try again.")
        root.destroy()
        return

#Test Script
if __name__ == "__main__":  
    source_dirname = "../../1_Place_Reports_Here" 
    check_file_counts_2S(source_dirname)