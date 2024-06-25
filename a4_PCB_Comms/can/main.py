import can 
from can.interface import Bus

vector_bus = can.Bus(interface='vector', channel=2, app_name="CANalyzer", bitrate=250000)