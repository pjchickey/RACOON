import serial
import time

def commandArduino(command, retries=50):
    status = 2 #2- No acknowledgement receieved; 1 - No completion code recieved; 0 - Command successfully executed
    SUCCESS = 0  #Success code
    COMMANDS = {1:("Sort to Trash", 1000), 2:("Sort to Recycling", 1000)}     #code: (desc, number of retries for getting completion code)
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
                status = 1
                print(f"Command {command} acknowledged!")
                break
            else:
                raise RuntimeError(f"Recieved bad response from Arduino: {line}. Expected {command}")
    if status == 2:
        raise TimeoutError(f"Failed to communicate with Arduino after {retries} attempts")
    ser.flush()
    for i in range(COMMANDS[command][1]):   #Wait for Arduino response that it completed the task
        line = ser.readline().decode('utf-8').rstrip()
        line.replace(" ", "")
        line.replace("\n", "")
        line.replace("\t", "")
        if(line != ""):
            print(line)
            if(line == SUCCESS):
                status = 0  #command complete
                break   
            elif(line != command):  #Check that Arduino isn't still sending acknowledgement
                raise RuntimeError(f"Something went wrong when completing command {command}: {COMMANDS[command][0]}.")
    if status == 1:
        raise TimeoutError(f"Failed to hear command response from Arduino after {COMMANDS[command][1]} attempts")
    else:
        print("Task complete.")
        
if __name__ == '__main__':
    commandArduino("0")    
