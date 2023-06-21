import serial
import time

ser = serial.Serial ("COM5", 9600)
if ser.isOpen () == False:
    ser.open ()

def sendSMS (msg):
    ser.write ("AT\r\n".encode())
    print ("AT")
    time.sleep (2)
    ser.write ("AT+W\r\n".encode())
    print ("AT+W")
    time.sleep (2)
    ser.write ("AT+CMGF=1\r\n".encode())
    print ("AT+CMGF=1")
    time.sleep (2)
    ser.write ("AT+CMGS=\"9847969644\"\r\n".encode())
    print ("AT+CMGS=\"9847969644\"")
    time.sleep (2)
    ser.write (msg.encode())
    print (msg)
    time.sleep (2)

    ser.write (chr(26).encode())
    print (chr(26))
    time.sleep (5)

sendSMS ("ok")
ser.close ()
