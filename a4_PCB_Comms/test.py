import serial

from serial import tools

print([comport.device for comport in serial.tools.list_ports.comports()])
