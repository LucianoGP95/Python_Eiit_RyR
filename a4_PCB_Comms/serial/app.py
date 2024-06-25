import serial
import serial.tools.list_ports
import threading
import tkinter as tk
from tkinter import ttk

class ArduinoCommunicationApp:
    def __init__(self, master, COM):
        self.master = master
        self.master.title("Arduino Communication App")
        self.serial_port = serial.Serial(COM, 9600, timeout=1)
        self.create_widgets()

    def create_widgets(self):
        self.message_entry = ttk.Entry(self.master, width=40)
        self.message_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.send_button = ttk.Button(self.master, text="Send Message", command=self.send_message)
        self.send_button.grid(row=1, column=0, pady=10, columnspan=2)
        self.receive_label = ttk.Label(self.master, text="Received Message:")
        self.receive_label.grid(row=2, column=0, pady=10, columnspan=2)
        self.receive_text = tk.Text(self.master, height=5, width=40)
        self.receive_text.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

    def send_message(self):
        message = self.message_entry.get()
        self.serial_port.write(message.encode('utf-8'))

    def read_serial(self):
        print("Hello")
        while True:
            if self.serial_port.in_waiting > 0:
                received_data = self.serial_port.readline().decode('utf-8')
                self.receive_text.insert(tk.END, received_data)
                self.master.update_idletasks()

#Test script
if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoCommunicationApp(root)

    # You can start a separate thread for reading serial data continuously
    # Uncomment the following lines if you want to continuously read and display received data
    # import threading
    # serial_thread = threading.Thread(target=app.read_serial)
    # serial_thread.start()

    root.mainloop()
