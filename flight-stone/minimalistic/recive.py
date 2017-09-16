import serial

#python -m serial.tools.list_ports
ser = serial.Serial("/dev/ttyUSB0",9600)
print("Init")
while(True):
    print("MSG: " + ser.readline().decode('utf-8') )
