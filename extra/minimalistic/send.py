import serial

ser = serial.Serial("/dev/ttyUSB0",9600)
print("Init")

while(True):
    msg = input("CHAR: ") or 'Jorge is your master'
    msg = msg*100
    for c in msg:
        c = c.encode('utf-8')
        print(c)
        ser.write(c)
        a = ser.readline().decode('utf-8')
        if a.split('[')[1][0].encode('utf-8') != c:
            print(a,c)
            print('ERROR')
            break
        print(a)
