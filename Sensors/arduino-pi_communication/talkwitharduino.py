import serial
import time

def commandArduino(command):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        ser.write(bytes(command, 'utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        line.replace(" ", "")
        line.replace("\n", "")
        line.replace("\t", "")
        if(line != ""):
            print(line)
            break

if __name__ == '__main__':
    commandArduino("0")    
