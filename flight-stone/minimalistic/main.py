import serial
import time

#python -m serial.tools.list_ports
ser = serial.Serial("/dev/ttyUSB0")
ser.baudrate = 10417
print("Init")
while(True):
    print(ser.readline())
