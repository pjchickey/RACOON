import RPi.GPIO as GPIO
from time import sleep

pin = 12

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
pwm=GPIO.PWM(pin, 50)
pwm.start(0)

def setAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(pin, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(pin, False)
	pwm.ChangeDutyCycle(0)

if __name__ == "__main__":
    setAngle(180)
    pwm.stop()
    GPIO.cleanup()
