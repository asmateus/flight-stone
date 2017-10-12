import serial

comands = {
    "start"     : "xsxxxxxx",
    "up"        : "xmu124xx",
    "down"      : "xmd124xx",
    "left"      : "xml124xx",
    "right"     : "xmr124xx",
    "forward"   : "xmf124xx",
    "backwards" : "xmb124xx",
    "rotleft"   : "xrl124xx",
    "rotright"  : "xrr124xx"
}

ser = serial.Serial("/dev/ttyUSB0",9600)
print("Init")

while(True):
    try:
        msg = input("Ingrese Comando: ")
        print("Send: "+comands[msg])
        ser.write(comands[msg].encode())
        print("PIC : "+ser.readline().decode('utf-8'))
    except KeyError:
        print("Error")


print("END")
