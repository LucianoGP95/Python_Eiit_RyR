def askdirectory():
    source_dirname = tk.filedialog.askdirectory()
    text1.delete(0, tk.END)
    text1.insert(0, string)
    return source_dirname

def asktarget():
    target_dirname = tk.filedialog.askopenfilename()
    text2.delete(0, tk.END)
    text2.insert(0, string)
    return target_dirname