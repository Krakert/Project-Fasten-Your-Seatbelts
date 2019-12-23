import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)

#defines
GPIO_TRIGGER = 13
GPIO_ECHO = 26
MAX_MESURE_DISTANCE = 400 #cm
SOUND_OF_SPEED = 34300 #cm/s
TIMEOUT = 250 #ms

#GPIO setup
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
#this function returns the measured distance in cm
#if te returned value= 0 the value is nog valid
def distance():
    #send pulse
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    startTime = 0
    stopTime = 0
    currentTime = time.time() * 1000 #used for timeout

    while GPIO.input(GPIO_ECHO) == 0:
        if((currentTime + TIMEOUT) < (time.time() * 1000)):
            print('FAILED sonar step 1')
            return 0
        startTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        if((currentTime + TIMEOUT) < (time.time() * 1000)):
            print('FAILED sonar step 2')
            return 0
        stopTime = time.time()
 
    #calculate the distance
    distance = ((stopTime - startTime) * 34300) / 2

    #return 0 if the value is not valid
    if distance > MAX_MESURE_DISTANCE:
        distance = 0
 
    return distance
 
