import serial
import threading
import tkinter as tk
from tkinter import ttk
from app import ArduinoCommunicationApp

root = tk.Tk()
app = ArduinoCommunicationApp(root, "COM7")
serial_thread = threading.Thread(target=app.read_serial)
serial_thread.start()

root.mainloop()