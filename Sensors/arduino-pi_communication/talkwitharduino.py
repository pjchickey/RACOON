import serial
import time

def commandArduino(command, retries=50):
    COMMANDS = {0:("Sort to Trash", 0, 500), 1:("Sort to Recycling", 0, 500)}     #code: (desc, success exit code, timeout for completion in seconds)
    print(COMMANDS[command][0])
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    for i in range(retries):
        ser.write(bytes(command, 'utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        line.replace(" ", "")
        line.replace("\n", "")
        line.replace("\t", "")
        if(line != ""):
            print(line)
            if(line == command):    #command acknowledged, arduino has started action
                ser.flush()
                for i in range(COMMANDS[command][2]):
                    line = ser.readline().decode('utf-8').rstrip()
                    line.replace(" ", "")
                    line.replace("\n", "")
                    line.replace("\t", "")
                    if(line != ""):
                        print(line)
                        if(line == COMMANDS[command][1]):
                            break   #command complete
                        else:
                            raise RuntimeError(f"Something went wrong when completing command {command}: {COMMANDS[command][0]}.")
            
    

if __name__ == '__main__':
    commandArduino("0")    
