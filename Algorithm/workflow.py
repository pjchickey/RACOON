# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""label_image for tflite."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import time

import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite # TF2
import cv2
import picamera

import threading
import os
import barcode
import sys
#import pseudo_motor
#import serial

import update_db
import talkwitharduino

import time

# servo imports
import RPi.GPIO as GPIO
from time import sleep

#servo setup
SERVO_PIN = 18
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

SWITCH_PIN = 15           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(SWITCH_PIN, GPIO.IN)           # Set our input pin to be an input

global code
code = None

def check_switch():
    if (GPIO.input(SWITCH_PIN) == True): # Physically read the pin now
        switchStatus = 0
    else:
        switchStatus = 1
    
    return switchStatus

def lock_door():
    pwm=GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)
    
    duty = 0 / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)
    
    pwm.stop()
    #GPIO.cleanup()
    
    return 0

def unlock_door():
    pwm=GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)
    
    duty = 180 / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)
    
    pwm.stop()
    #GPIO.cleanup()
    
    return 0

def read_barcode():
    #global code
    #code = None
    #time.sleep(5)

    try: 
        code = barcode.barcode_reader()
    except PermissionError:
        os.system('sudo chmod 777 /dev/hidraw1')
        print('caught PermissionError')
        code = barcode.barcode_reader()
    print(code)
    valid_code = code.startswith('racoon_')
    print(str(valid_code) + ' valid code')

    if valid_code == False:
        code = None
    elif valid_code == True:
        print("valid code: " + code) 

def classify_model():
    model_file = 'racoon01.tflite'
    #label_file = '/home/pi/RACOON/Algorithm/labels.txt'

    #print(model_file)
    interpreter = tflite.Interpreter(model_path=model_file)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # check the type of the input tensor
    floating_model = input_details[0]['dtype'] == np.float32

    with picamera.PiCamera() as camera:
        camera.resolution = (224, 224)
        camera.framerate = 24
        time.sleep(2)
        image = np.empty((224 * 224 * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        img = image.reshape((224, 224, 3))
        

    # NxHxWxC, H:1, W:2
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    #img = cv2.imread('Images/Recycle/7upsmallcan8--10.png')     #unnecessary bc image is already a numpy array
    #img = cv2.resize(img, (width, height))
    cv2.imwrite('test.png', img)

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data))

    interpreter.set_tensor(input_details[0]['index'], input_data)

    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)    

    if results[0] > 0.8:
        print("Recycle")
        is_recyclable = True
    else:
        print('Trash')
        is_recyclable = False

    #print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))

    return is_recyclable

def main():

    SERVO_PIN = 18
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    SWITCH_PIN = 15           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
    GPIO.setup(SWITCH_PIN, GPIO.IN)           # Set our input pin to be an input

    # temporary number
    #x = True

    time_check = 100

    #for limit switch, 0 - open door, 1 - closed door

    # poll limit switch continuously 
    #limit_switch = talkwitharduino.commandArduino(5)
    while True:
        limit_switch = check_switch()
        print('checking if limit switch is 0')
        
        if limit_switch is 0:
            break

        time.sleep(0.5)

    
    # wait a bit for object to go into receptacle
    time.sleep(2)

    # check initial weight and times
    #load_cell_weight = talkwitharduino.commandArduino(6)
    start_time = time.time()
    end_time = time.time()

    # check load cell value
    # no load cell weight use
    '''
    while True:
        load_cell_weight = talkwitharduino.commandArduino(6)
        
        end_time = time.time()

        print("checking if load cell is 1")
        if load_cell_weight is 1:
            print(load_cell_weight)
            break

        # check if the time elapsed between limit switch and load cell is below limit
        if (end_time - start_time) > time_check:
            break
    print('checking')
    # if load cell is still nothing, return to beginning
    if load_cell_weight is 0:
        x = False

    # if time elapsed is enough, return to beginning
    if (end_time - start_time) > time_check:
        x = False 
    '''
    # check and lock hinge
    num_door_check = 0

    while True:
        print('checking if limit switch is 1')
        limit_switch = check_switch()
        #limit_switch = 1
        end_time = time.time()

        # check if closed door is stable
        if limit_switch is 1:
            num_door_check = num_door_check + 1
        elif limit_switch is 0:
            num_door_check = 0
        
        #if door is confirmed closed, break out of checking closed door
        if num_door_check > 10:
            break
        
        # time check on door
        # if not door, completely stop code, throw error
        if (end_time - start_time) > time_check:
            #x = False
            print('core dump, door lock mechanism is fucked')
            sys.exit()
            break

        time.sleep(0.1)
    
    # may not need if x statement
    # was used when load cell was integrated
    #if x:

    lock_door()

    result = classify_model()

    if result:
        talkwitharduino.commandArduino(4)
    else:
        talkwitharduino.commandArduino(3)


    #dummy_sort(result)

if __name__ == '__main__':
    unlock_door()
    loop_try = 0

    SERVO_PIN = 18
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    SWITCH_PIN = 15           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
    GPIO.setup(SWITCH_PIN, GPIO.IN)           # Set our input pin to be an input

    while True:

        SERVO_PIN = 18
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)

        SWITCH_PIN = 15           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
        GPIO.setup(SWITCH_PIN, GPIO.IN)           # Set our input pin to be an input
    
        #classify_thread = threading.Thread(target=lambda q, arg1: q.put(classify_model(arg1)), args=(que, 'nothing'))
        
        classify_and_sort_thread = threading.Thread(target=main, args=[])

        #set barcode thread to be daemon so it is terminated when classify thread is finished
        barcode_thread = threading.Thread(target=read_barcode, args=[], daemon=True)

        #classify_thread.start()
        classify_and_sort_thread.start()
        barcode_thread.start()

        classify_and_sort_thread.join()
        
        #structural print, do not remove
        print(code)

        #print(result)
        if code == None:
            print('no user')
        else:
            print('user is ' + code)
            update_db.main(code)
        #send_to_arduino(result)

        #while !(read_from_arduino()):
        #    read_from_arduino()

        loop_try = loop_try + 1
        unlock_door()
        print("///////////////system has cycled " + str(loop_try) + ' times/////////////////')