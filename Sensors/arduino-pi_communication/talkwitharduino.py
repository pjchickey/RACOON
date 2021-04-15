import serial
import time

def commandArduino(command, retries=50):
    status = 2 #2- No acknowledgement receieved; 1 - No completion code recieved; 0 - Command successfully executed 
    COMMANDS = {0:("Sort to Trash", 0, 500), 1:("Sort to Recycling", 0, 500)}     #code: (desc, success exit code, number of retries for getting completion code)
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
                            status = 0  #command complete
                            break   
                        else:
                            raise RuntimeError(f"Something went wrong when completing command {command}: {COMMANDS[command][0]}.")
                if status == 0:
                    break
                else:
                    raise TimeoutError(f"Maximum attempts of {COMMANDS[command][2]} exceeded for command {command}.")
            else:
                raise RuntimeError(f"Recieved bad response from Arduino: {line}")
    if status == 0:
        print("Task complete.")
    elif status == 1:
        raise RuntimeError(f"Command {command} acknowledged by Arduino, but task failed to complete.")
    else:
        raise RuntimeError(f"Command {command} failed successfully.")  
            
            
    

if __name__ == '__main__':
    commandArduino("0")    
