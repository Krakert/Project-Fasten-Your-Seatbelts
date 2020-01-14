#!/usr/bin/env python3

#import installed libraries
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#defines
GPIO_TRIGGER = 26
GPIO_ECHO = 20
MAX_MESURE_DISTANCE = 400 #cm
SPEED_OF_SOUND = 34300 #cm/s
TIMEOUT = 250 #ms

#GPIO setup
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
#this function returns the measured distance in cm
#if te returned value= 0 the value is not valid
def distance():
    GPIO.output(GPIO_TRIGGER, True)                                 # Send a pulse of 1 nanosecond.
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    startTime = 0
    stopTime = 0
    currentTime = time.time() * 1000                                # Used for timeout.

    while GPIO.input(GPIO_ECHO) == 0:
        if (currentTime + TIMEOUT) < (time.time() * 1000):          # If pulse is not not registered return a 0.
            return 150
        startTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        if (currentTime + TIMEOUT) < (time.time() * 1000):          # If pulse is not not registered return a 0.
            return 200
        stopTime = time.time()
 
    distance = ((stopTime - startTime) * SPEED_OF_SOUND) / 2        # Calculate the distance.


    if distance > MAX_MESURE_DISTANCE:                              # The sonar is capable of measure up to 400 cm.
        distance = 0                                                # Return 0 if the value is not valid.
 
    return distance