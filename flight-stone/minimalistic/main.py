import serial
import time

#python -m serial.tools.list_ports

ser = serial.Serial("/dev/ttyUSB0")
while(True):
    print(ser.readline())
    time.sleep(2)
