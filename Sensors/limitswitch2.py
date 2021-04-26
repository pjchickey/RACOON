from time import sleep           # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO
 
GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
SWITCH_PIN = 15           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(SWITCH_PIN, GPIO.IN)           # Set our input pin to be an input

# Start a loop that never ends
def readLimitSwitch():
    if (GPIO.input(SWITCH_PIN) == True): # Physically read the pin now
        switchStatus = 1
    else:
        switchStatus = 0
    
    return switchStatus

print(readLimitSwitch)

