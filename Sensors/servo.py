import RPI.GPIO as GPIO
from time import sleep

pin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
pwm=GPIO.PWM(pin, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(pin, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(pin, False)
	pwm.ChangeDutyCycle(0)

if __name__ == "main":
    SetAngle(90) 
    pwm.stop()
    GPIO.cleanup()