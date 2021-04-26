import RPi.GPIO as GPIO
from time import sleep

def lockDoor():
    pwm_pin = 12
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwm_pin, GPIO.OUT)
    pwm=GPIO.PWM(pwm_pin, 50)
    pwm.start(0)
    
    duty = 0 / 18 + 2
    GPIO.output(pwm_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(pwm_pin, False)
    pwm.ChangeDutyCycle(0)
    
    pwm.stop()
    GPIO.cleanup()
    
    return 0

def unlockDoor():
    pwm_pin = 12
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwm_pin, GPIO.OUT)
    pwm=GPIO.PWM(pwm_pin, 50)
    pwm.start(0)
    
    duty = 180 / 18 + 2
    GPIO.output(pwm_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(pwm_pin, False)
    pwm.ChangeDutyCycle(0)
    
    pwm.stop()
    GPIO.cleanup()
    
    return 0

if __name__ == "__main__":
    lockDoor()
    sleep(1)
    unlockDoor()
    sleep(1)
    lockDoor()
