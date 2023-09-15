import serial

port = 'COM14'
baud_rate = 9600

ser = serial.Serial(port, baud_rate)

# Sending data
data_to_send = b'Hello, MCU!'
ser.write(data_to_send)

# Receiving data
received_data = ser.read(10)  # Read up to 10 bytes of data
print("Received:", received_data)

ser.close()
