import serial

ser = serial.Serial("/dev/ttyUSB0",9600)
print("Init")

while(True):
    msg = "axsxxaxx"
    print("Command : "+msg)
    ser.write(msg.encode())
    a = ser.readline().decode('utf-8')
    print("recive  : "+a)
