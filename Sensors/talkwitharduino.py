import serial
import time

from serial.serialutil import SerialException

def commandArduino(command, retries=50):
    status = 2 #2- No acknowledgement received; 1 - No completion code received; 0 - Command successfully executed
    #{command code: (desc, type of response, number of retries for getting a completion)}
    #type of response - 0: Success code expected; 1: Binary result expected; 2: Any integer value expected
    COMMANDS = {3:("Sort to Trash", 0, 1000), 
                4:("Sort to Recycling", 0, 1000), 
                5:("Read Hinge State (Limit Switch)", 1, 100), 
                6:("In-Device Object Detection (load cell)", 1, 100), 
                7:("Read Sensor value", 2, 100)}          
    print(COMMANDS[command][0])
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except SerialException:
        raise SerialException("Could not find Arduino at port /dev/ttyACM0")
    ser.flush()
    for i in range(retries):
        ser.write(bytes(str(command), 'ascii'))
        ser.write(b"\n")
        line = ser.readline().decode('utf-8').rstrip()
        line.replace(" ", "")
        line.replace("\n", "")
        line.replace("\t", "")
        if(line != ""):
            resp = int(line)
            if(resp == command):    #command acknowledged, arduino has started action
                status = 1
                print(f"Command acknowledged after {i} attempts.")
                break
            else:
                raise RuntimeError(f"Bad response from Arduino: Expected command {command}, but received {resp}")
    if status == 2:
        raise TimeoutError(f"Failed to communicate with Arduino after {retries} attempts")
    ser.flush()
    for i in range(COMMANDS[command][2]):   #Wait for Arduino response that it completed the task
        line = ser.readline().decode('utf-8').rstrip()
        line.replace(" ", "")
        line.replace("\n", "")
        line.replace("\t", "")
        if(line != ""):
            resp = int(line)
            resp_prefix = int(line[0])
            if resp == command:
                continue    #Arduino is still sending acknowledgement 
            if resp_prefix == 0:    #Success code
                if resp == 0 and COMMANDS[command][1] == 0:
                    status = 0
                    print(f"{COMMANDS[command][0]} completed successfully!\nRecieved task completion after {i} communication attempts")
                    return None
                else:
                    raise ValueError(f"Got unexpected response {resp}.")
            elif resp_prefix == 1:  #Error code
                raise RuntimeError(f"Something went wrong when attempting to complete command {command}: {COMMANDS[command][0]}.\nReturn code: {resp}")
            elif resp_prefix == 2:  #Any value
                value = int(line[1:])
                if COMMANDS[command][1] == 1:   #Binary response expected
                    if value == 0 or value == 1:
                        status = 0
                        print(f"{COMMANDS[command][0]} completed successfully!\nValue Received: {value} \nReceived task completion after {i} communication attempts")
                        return value
                    else:
                        raise ValueError(f"Got unexpected value {value} when expecting binary response.")   
                else:   #Any integer value expected
                    status = 0
                    print(f"{COMMANDS[command][0]} completed successfully!\nValue Received: {value} \nReceived task completion after {i} communication attempts")
                    return value    
            else:
                raise ValueError(f"Got unexpected prefix '{resp_prefix}' as part of response '{resp}'.")
                
    if status == 1:
        raise TimeoutError(f"Failed to hear command response from Arduino after {COMMANDS[command][2]} attempts")
        
if __name__ == '__main__':
    output = commandArduino(3)
    if not(output is None):
        print(output)
    time.sleep(1)
    output = commandArduino(4)    
